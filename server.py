import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Gemini API key from environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")
print(f"API Key found: {bool(API_KEY)}")  # Debug print

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    print("Gemini AI configured successfully")
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    model = None

# Root route for browser check
@app.route("/")
def home():
    return "HealthGuardianAI backend is running."

# Health check endpoint
@app.route("/health")
def health():
    if model:
        return jsonify({"status": "healthy", "gemini_configured": True})
    else:
        return jsonify({"status": "unhealthy", "gemini_configured": False}), 500

# AI chat route
@app.route("/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
        
    try:
        # Check if model is configured
        if not model:
            return jsonify({"error": "Gemini AI not configured properly"}), 500
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        print(f"Received message: {user_message}")
        response = model.generate_content(user_message)
        
        if not response.text:
            return jsonify({"error": "Empty response from Gemini"}), 500
            
        return jsonify({"response": response.text})
        
    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
