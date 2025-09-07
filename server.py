from flask import Flask, request, Response
from flask_cors import CORS
import google.generativeai as genai
import os
API_KEY = os.getenv("AIzaSyCqS9615Ggp1g7CvXmbEO-T4L9wUs4e9hE")
genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message", "")

    def generate():
        model = genai.GenerativeModel("gemini-1.5-flash")
        stream = model.generate_content(
            [user_message],
            stream=True
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text

    return Response(generate(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)

