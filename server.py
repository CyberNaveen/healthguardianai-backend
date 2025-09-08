import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Gemini API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")  # Changed to use environment variable
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=API_KEY)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["*"])  # Explicitly allow all origins for now

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# Root route for browser check
@app.route("/")
def home():
    return "HealthGuardianAI backend is running."

# AI chat route
@app.route("/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Health check endpoint
@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
