from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import os
from dotenv import load_dotenv
from mcp_client import SustainableEcoMCPClient

load_dotenv('.env', override=True)

app = Flask(__name__)
CORS(app)

# Initialize MCP client with Ollama
mcp_client = SustainableEcoMCPClient(llm_provider="ollama", model="llama3.1:8b")

# Event loop for async operations
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Connect to MCP server on startup
def connect_mcp():
    """Connect to MCP server on application startup."""
    try:
        loop.run_until_complete(mcp_client.connect("mcp_server.py"))
        print("MCP client connected successfully")
    except Exception as e:
        print(f"Failed to connect MCP client: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "chat-backend-mcp"})

@app.route('/chat', methods=['POST'])
def chat():
    """Enhanced chat endpoint that uses MCP for sustainability queries."""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Check if the message is related to sustainability/building data
        sustainability_keywords = [
            'energy', 'consumption', 'sustainability', 'carbon', 'footprint',
            'water', 'usage', 'building', 'metrics', 'eco', 'environmental',
            'recommend', 'analyze', 'report', 'statistics'
        ]
        
        is_sustainability_query = any(keyword in user_message.lower() for keyword in sustainability_keywords)
        
        if is_sustainability_query and mcp_client.agent:
            # Use MCP client for sustainability queries
            try:
                # Run async query in sync context
                ai_message = loop.run_until_complete(mcp_client.query(user_message))
                
                return jsonify({
                    "message": ai_message,
                    "model": "llama3.1:8b (via MCP)",
                    "status": "success",
                    "mcp_enabled": True
                })
            except Exception as e:
                print(f"MCP query failed: {e}")
                # Fallback to regular Ollama if MCP fails
        
        # For non-sustainability queries or if MCP fails, use regular Ollama
        import requests
        
        OLLAMA_URL = "http://localhost:11434/api/generate"
        MODEL_NAME = "llama3.1"
        
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
                "status": "success",
                "mcp_enabled": False
            })
        else:
            return jsonify({
                "error": "Failed to get response from Ollama",
                "status_code": response.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """Dedicated endpoint for sustainability analysis using MCP."""
    try:
        data = request.get_json()
        analysis_type = data.get('type', 'general')
        
        if not mcp_client.agent:
            return jsonify({"error": "MCP client not connected"}), 503
        
        if analysis_type == 'period':
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            
            if not start_date or not end_date:
                return jsonify({"error": "start_date and end_date required"}), 400
            
            result = loop.run_until_complete(
                mcp_client.analyze_period(start_date, end_date)
            )
            
        elif analysis_type == 'recommendations':
            result = loop.run_until_complete(
                mcp_client.get_recommendations()
            )
            
        elif analysis_type == 'compare':
            period1_start = data.get('period1_start')
            period1_end = data.get('period1_end')
            period2_start = data.get('period2_start')
            period2_end = data.get('period2_end')
            
            if not all([period1_start, period1_end, period2_start, period2_end]):
                return jsonify({"error": "All period dates required"}), 400
            
            result = loop.run_until_complete(
                mcp_client.compare_periods(
                    period1_start, period1_end,
                    period2_start, period2_end
                )
            )
            
        else:
            # General analysis with custom query
            query = data.get('query', 'Provide a general sustainability analysis')
            result = loop.run_until_complete(mcp_client.query(query))
        
        return jsonify({
            "result": result,
            "analysis_type": analysis_type,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": "Analysis failed",
            "details": str(e)
        }), 500

@app.route('/models', methods=['GET'])
def get_models():
    """Get available models including MCP status."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        
        models_data = {"models": []}
        
        if response.status_code == 200:
            models_data = response.json()
        
        # Add MCP status
        models_data["mcp_enabled"] = mcp_client.agent is not None
        models_data["mcp_model"] = "llama3.1:8b" if mcp_client.agent else None
        
        return jsonify(models_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Connect to MCP server before starting Flask
    connect_mcp()
    
    # Run Flask app
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)