from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# ⚠️ Hardcode Gemini API key (only for testing!)
API_KEY = "AIzaSyCqS9615Ggp1g7CvXmbEO-T4L9wUs4e9hE"

# Configure Gemini
genai.configure(api_key=API_KEY)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Root route
@app.route("/")
def home():
    return "HealthGuardianAI backend is running."

# AI chat route
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = model.generate_content(user_message)
        reply = response.text if hasattr(response, "text") else str(response)
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

