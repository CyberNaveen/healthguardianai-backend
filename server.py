import os
from flask import Flask, request, Response
from flask_cors import CORS
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Gemini API key from environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=API_KEY)

@app.route("/")
def home():
    return "HealthGuardianAI backend is running."

@app.route("/health")
def health():
    return "Server is healthy"

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        return Response(status=200)
        
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return {"error": "No message provided"}, 400

        # Use the same model that works locally
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        def generate():
            try:
                stream = model.generate_content([user_message], stream=True)
                for chunk in stream:
                    if chunk.text:
                        yield chunk.text
            except Exception as e:
                yield f"Error: {str(e)}"

        return Response(generate(), mimetype="text/plain")
        
    except Exception as e:
        return {"error": f"Internal server error: {str(e)}"}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
