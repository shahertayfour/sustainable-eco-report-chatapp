from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv('.env', override=True)

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "chat-backend"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        ollama_payload = {
            "model": MODEL_NAME,
            "prompt": user_message,
            "stream": False
        }
        
        response = requests.post(OLLAMA_URL, json=ollama_payload, timeout=30)
        
        if response.status_code == 200:
            ollama_response = response.json()
            ai_message = ollama_response.get('response', '')
            return jsonify({
                "message": ai_message,
                "model": MODEL_NAME,
                "status": "success"
            })
        else:
            return jsonify({
                "error": "Failed to get response from Ollama",
                "status_code": response.status_code
            }), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Connection error to Ollama service",
            "details": str(e)
        }), 503
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/models', methods=['GET'])
def get_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch models"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)