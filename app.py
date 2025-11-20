from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    direction = data.get("direction", "en-so")

    instruction = "English to Somali" if direction == "en-so" else "Somali to English"

    response = client.responses.create(
        model="gpt-5-nano",
        input=f"Translate this {instruction}: {text}",
    )

    translation = response.output_text
    return jsonify({"translation": translation})

@app.route("/", methods=["GET"])
def home():
    return "Translation API is running."

if __name__ == "__main__":
    app.run()
