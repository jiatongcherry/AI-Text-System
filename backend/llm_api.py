from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Define req function to call SiliconFlow API
def req(system: str, user: str) -> str:
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("SILICONFLOW_BASE_URL")
    )
    response = client.chat.completions.create(
        model='deepseek-ai/DeepSeek-R1',
        messages=[
            {'role': "system", 'content': system},
            {'role': "user",   'content': user}
        ],
        max_tokens=4096
    )
    return response.choices[0].message.content.strip()

# 2. Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app, resources={
    r"/extract_keywords": {"origins": "http://localhost:5173"},
    r"/summarize":        {"origins": "http://localhost:5173"},
    r"/classify_topic":  {"origins": "http://localhost:5173"}
})

# 3. Keyword extraction endpoint
@app.route("/extract_keywords", methods=["POST"])
def extract_keywords():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data  = request.get_json()
    text  = data.get("text", "")
    top_n = data.get("top_n", 5)

    # Log input
    print(f"[extract_keywords] Received text: {text!r}")
    print(f"[extract_keywords] top_n: {top_n}")

    # Input validation
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Text must be a non-empty string"}), 400
    if not isinstance(top_n, int) or top_n < 1:
        return jsonify({"error": "top_n must be a positive integer"}), 400

    # Construct prompt
    system_prompt = (
        "You are an English keyword extraction expert. "
        "Return only a JSON array containing the extracted keyword strings."
    )
    user_prompt = (
        f"Extract the top {top_n} most important keywords from the following text:\n\n"
        f"\"\"\"\n{text}\n\"\"\""
    )

    try:
        resp_text = req(system_prompt, user_prompt)

        # Log raw model output
        print(f"[extract_keywords] Raw LLM response: {resp_text!r}")

        # Parse model response as JSON list
        try:
            keywords = json.loads(resp_text)
        except json.JSONDecodeError:
            # Fallback parsing
            keywords = [w.strip(' "\'') for w in resp_text.strip().strip('[]').split(',') if w.strip()]

        # Log final keywords
        print(f"[extract_keywords] Parsed keywords: {keywords}")

        return jsonify({"keywords": keywords}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to extract keywords: {str(e)}"}), 500

# 4. Text summarization endpoint
@app.route("/summarize", methods=["POST"])
def summarize():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data  = request.get_json()
    text  = data.get("text", "")
    ratio = data.get("ratio", 0.3)

    # Log input
    print(f"[summarize] Received text: {text!r}")
    print(f"[summarize] ratio: {ratio}")

    # Input validation
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Text must be a non-empty string"}), 400
    if not isinstance(ratio, (int, float)) or ratio <= 0 or ratio > 1:
        return jsonify({"error": "Ratio must be a number between 0.1 and 1"}), 400

    # Estimate desired summary length
    word_count = len(text.split())
    approx_len = max(20, int(word_count * ratio))

    # Construct prompt
    system_prompt = "You are an English summarization expert. Output only the summary content, without additional explanations."
    user_prompt = (
        f"Generate a summary of approximately {approx_len} words for the following text:\n\n"
        f"\"\"\"\n{text}\n\"\"\""
    )

    try:
        summary = req(system_prompt, user_prompt)
        # Log raw model output
        print(f"[summarize] Raw LLM response: {summary!r}")
        # Log final summary
        print(f"[summarize] Final summary: {summary}")
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to generate summary: {str(e)}"}), 500

# Topic classification endpoint
@app.route("/classify_topic", methods=["POST"])
def classify_topic():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    text = data.get("text", "")

    # Log input
    print(f"[classify_topic] Received text: {text!r}")

    # Input validation
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Text must be a non-empty string"}), 400

    # Predefined topics
    topics = [
        "sports",
        "politics",
        "technology",
        "entertainment",
        "health",
        "business",
        "science",
        "education",
        "environment",
        "culture",
        "building"
    ]

    # Construct prompt
    system_prompt = (
        "You are an English text classification expert. "
        "Your task is to classify the input text into one of the following topics: sports, politics, technology, entertainment, health, business, science, education, environment, culture, building. "
        "Return only the topic name as a single string, nothing else."
    )
    user_prompt = (
        f"Classify the following text into one of these topics (sports, politics, technology, entertainment, health, business, science, education, environment, culture, building):\n\n"
        f"\"\"\"\n{text}\n\"\"\""
    )

    try:
        topic = req(system_prompt, user_prompt)
        # Log raw model output
        print(f"[classify_topic] Raw LLM response: {topic!r}")

        # Validate the predicted topic
        if topic.lower() not in topics:
            return jsonify({"error": f"Invalid topic predicted: {topic}. Must be one of {topics}"}), 500

        # Log final topic
        print(f"[classify_topic] Predicted topic: {topic}")
        return jsonify({"topic": topic}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to classify topic: {str(e)}"}), 500

# 5. Start the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)