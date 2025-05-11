from flask import Flask, request, jsonify
from flask_cors import CORS
from text_processor import KeywordExtractor, TextSummarizer

app = Flask(__name__)
# Enable CORS for frontend (Vite runs on port 5173)
CORS(app, resources={r"/extract_keywords": {"origins": "http://localhost:5173"},
                     r"/summarize": {"origins": "http://localhost:5173"}})

# Initialize the processors
keyword_extractor = KeywordExtractor()
text_summarizer = TextSummarizer()

@app.route("/extract_keywords", methods=["POST"])
def extract_keywords():
    """Extract keywords from input text."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400
    
    text = data.get("text", "")
    top_n = data.get("top_n", 5)
    
    # Validate inputs
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Text must be a non-empty string"}), 400
    if not isinstance(top_n, int) or top_n < 1:
        return jsonify({"error": "top_n must be a positive integer"}), 400
    
    try:
        # Extract keywords
        keywords = keyword_extractor.extract_keywords(text, top_n)
        return jsonify({
            "keywords": [{"keyword": k, "score": float(s)} for k, s in keywords]
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to extract keywords: {str(e)}"}), 500

@app.route("/summarize", methods=["POST"])
def summarize():
    """Generate a summary of the input text."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400
    
    text = data.get("text", "")
    ratio = data.get("ratio", 0.3)
    
    # Validate inputs
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Text must be a non-empty string"}), 400
    if not isinstance(ratio, (int, float)) or ratio <= 0 or ratio > 1:
        return jsonify({"error": "Ratio must be a number between 0 and 1"}), 400
    
    try:
        # Generate summary
        summary = text_summarizer.summarize(text, ratio)
        return jsonify({"summary": summary}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate summary: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)