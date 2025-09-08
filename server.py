import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Gemini API key from environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")
logger.info(f"API Key found: {bool(API_KEY)}")

if not API_KEY:
    logger.error("GEMINI_API_KEY environment variable is required")
    raise ValueError("GEMINI_API_KEY environment variable is required")

try:
    genai.configure(api_key=API_KEY)
    
    # List available models to see what's working
    logger.info("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            logger.info(f"Available model: {m.name} - {m.supported_generation_methods}")
    
    # Try to find a working model
    model = None
    model_names_to_try = [
        "models/gemini-1.5-pro-latest",
        "models/gemini-1.0-pro",
        "models/gemini-pro"
    ]
    
    for model_name in model_names_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            logger.info(f"Successfully loaded model: {model_name}")
            break
        except Exception as e:
            logger.warning(f"Failed to load model {model_name}: {e}")
    
    if model:
        logger.info("Gemini AI configured successfully")
    else:
        logger.error("No working model found")
        model = None
        
except Exception as e:
    logger.error(f"Error configuring Gemini: {e}")
    model = None

# Root route for browser check
@app.route("/")
def home():
    return "HealthGuardianAI backend is running."

# Health check endpoint with model info
@app.route("/health")
def health():
    if model:
        return jsonify({"status": "healthy", "gemini_configured": True})
    else:
        return jsonify({"status": "unhealthy", "gemini_configured": False}), 500

# Model info endpoint
@app.route("/models")
def list_models():
    try:
        models = []
        for m in genai.list_models():
            models.append({
                "name": m.name,
                "supported_methods": m.supported_generation_methods
            })
        return jsonify({"models": models})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# AI chat route
@app.route("/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
        
    try:
        if not model:
            return jsonify({"error": "Gemini AI not configured properly"}), 500
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"Received message: {user_message}")
        response = model.generate_content(user_message)
        
        if not response.text:
            return jsonify({"error": "Empty response from Gemini"}), 500
            
        logger.info("Successfully generated response")
        return jsonify({"response": response.text})
        
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
