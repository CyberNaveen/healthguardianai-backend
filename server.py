from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os 

API_KEY = "AIzaSyCqS9615Ggp1g7CvXmbEO-T4L9wUs4e9hE"
genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

model = genai.GenerativeModel("models/gemini-2.5-flash")

@app.route("/")
def home():
    return "HealthGuardianAI backend is running."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return "No message provided", 400

    try:
        response = model.generate_content(user_message)
        reply = getattr(response, "text", None)
        if not reply and response.candidates:
            reply = response.candidates[0].content.parts[0].text
        return reply or "No reply generated.", 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        return str(e), 500, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
