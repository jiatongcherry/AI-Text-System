# mainbyllm.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import torch
from modelscope import AutoModelForCausalLM, AutoTokenizer


model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
model.eval()

def req_local(system: str, user: str) -> str:

    messages = [
        {"role": "system",  "content": system},
        {"role": "user",    "content": user}
    ]
    # Generate chat template
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    # encoding
    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=False
        )

    gen_ids = [out[len(inp):] for inp, out in zip(inputs.input_ids, outputs)]
    # Decoding
    return tokenizer.batch_decode(gen_ids, skip_special_tokens=True)[0].strip()

app = Flask(__name__)
CORS(app, resources={
    r"/extract_keywords": {"origins": "http://localhost:5173"},
    r"/summarize":        {"origins": "http://localhost:5173"}
})

@app.route("/extract_keywords", methods=["POST"])
def extract_keywords():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data  = request.get_json()
    text  = data.get("text", "")
    top_n = data.get("top_n", 5)

    print(f"[extract_keywords] text={text!r}, top_n={top_n}")

    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Text must be a non-empty string"}), 400
    if not isinstance(top_n, int) or top_n < 1:
        return jsonify({"error": "top_n must be a positive integer"}), 400

    system_prompt = (
        "你是一个中文关键词提取专家，"
        "只返回一个 JSON 数组，数组中是提取出的关键词字符串。"
    )
    user_prompt = (
        f"请从下面这段文本中提取最重要的 {top_n} 个关键词：\n\n"
        f"\"\"\"\n{text}\n\"\"\""
    )

    try:
        resp_text = req_local(system_prompt, user_prompt)
        print(f"[extract_keywords] Raw response: {resp_text!r}")

        try:
            keywords = json.loads(resp_text)
        except json.JSONDecodeError:
            keywords = [w.strip(' "\'') for w in resp_text.strip().strip('[]').split(',') if w.strip()]

        print(f"[extract_keywords] Parsed keywords: {keywords}")
        return jsonify({"keywords": keywords}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to extract keywords: {e}"}), 500

@app.route("/summarize", methods=["POST"])
def summarize():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data  = request.get_json()
    text  = data.get("text", "")
    ratio = data.get("ratio", 0.3)

    print(f"[summarize] text={text!r}, ratio={ratio}")

    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Text must be a non-empty string"}), 400
    if not isinstance(ratio, (int, float)) or ratio <= 0 or ratio > 1:
        return jsonify({"error": "Ratio must be a number between 0 and 1"}), 400

    word_count = len(text.split())
    approx_len = max(20, int(word_count * ratio))

    system_prompt = "你是一个中文摘要专家，输出直接就是摘要内容，不要多余说明。"
    user_prompt = (
        f"请为下面这段文本生成一段大约 {approx_len} 词左右的摘要：\n\n"
        f"\"\"\"\n{text}\n\"\"\""
    )

    try:
        summary = req_local(system_prompt, user_prompt)
        print(f"[summarize] Raw summary: {summary!r}")
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to generate summary: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
