import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_KEY      = os.getenv("AZURE_OPENAI_KEY")

app = Flask(__name__)
CORS(app)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    if not text:
        return jsonify({ 'error': 'No text provided.' }), 400

    headers = {
        'Content-Type': 'application/json',
        'api-key': AZURE_KEY
    }
    payload = {
        'messages': [
            { 'role': 'system', 'content': 'You are a helpful assistant that summarizes text.' },
            { 'role': 'user', 'content': f"Summarize the following text: {text}" }
        ]
    }
    resp = requests.post(AZURE_ENDPOINT, headers=headers, json=payload)
    data = resp.json()
    try:
        summary = data['choices'][0]['message']['content']
    except Exception:
        return jsonify({ 'error': 'Failed to parse response', 'details': data }), 500
    return jsonify({ 'summary': summary })

if __name__ == '__main__':
    app.run(debug=True)