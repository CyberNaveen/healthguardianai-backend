import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Load Gemini API key from environment variable
API_KEY = os.getenv("AIzaSyCqS9615Ggp1g7CvXmbEO-T4L9wUs4e9hE")
genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

model = genai.GenerativeModel("gemini-pro")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
