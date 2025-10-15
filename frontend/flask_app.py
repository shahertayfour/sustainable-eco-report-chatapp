import asyncio
import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from mcp_use import MCPAgent, MCPClient

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MCP Configuration for Building 413
MCP_CONFIG = {
    "mcpServers": {
        "sustainable-eco-report-chatapp": {
            "url": "http://localhost:4141/sse",
            "transport": "sse"
        }
    }
}

async def query_building_data(user_query):
    """Query Building 413 data using MCP agent"""
    try:
        # Create MCPClient from config
        client = MCPClient.from_dict(MCP_CONFIG)

        # Create Ollama LLM
        llm = ChatOllama(model="llama3.1", base_url="http://localhost:11434")

        # Create agent with the client
        agent = MCPAgent(llm=llm, client=client)

        # Initialize the agent (connects to MCP server and loads tools)
        await agent.initialize()

        # Pass the original user query directly to the agent
        # The agent will use the available MCP tools as needed
        result = await agent.run(user_query)
        return str(result)

    except Exception as e:
        return f"Error connecting to Building 413 data: {str(e)}"

def format_buildings_list():
    """Return information about Building 413"""
    return {
        "building_id": 413,
        "description": "Smart Building 413 - Environmental Monitoring System",
        "sensors": [
            "CO2 levels (air quality monitoring)",
            "Temperature readings",
            "Humidity measurements", 
            "Light/illumination levels",
            "PIR motion detection"
        ],
        "sample_queries": [
            "Get building energy stats for building 413",
            "Show me CO2 levels and air quality",
            "Analyze temperature and humidity",
            "What are the sustainability metrics?",
            "Calculate carbon footprint"
        ]
    }

@app.route('/')
def index():
    """Render the main chat interface"""
    building_info = format_buildings_list()
    return render_template('chat.html', building_info=building_info)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    # Handle local queries that don't need MCP
    if any(keyword in user_message.lower() for keyword in ['list', 'buildings', 'available', 'help']):
        building_info = format_buildings_list()
        response = f"""
🏢 **Building 413 Information**

**Building ID:** {building_info['building_id']}
**Description:** {building_info['description']}

📊 **Available Sensors:**
{chr(10).join(f"• {sensor}" for sensor in building_info['sensors'])}

💡 **Try these queries:**
{chr(10).join(f"• {query}" for query in building_info['sample_queries'])}

Ready to analyze Building 413 environmental data!
        """
        return jsonify({
            "response": response.strip(),
            "source": "local"
        })
    
    # Use MCP agent for data analysis queries
    try:
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(query_building_data(user_message))
        loop.close()
        
        return jsonify({
            "response": response,
            "source": "mcp_agent"
        })
        
    except Exception as e:
        return jsonify({
            "response": f"Sorry, I encountered an error analyzing Building 413 data: {str(e)}",
            "source": "error"
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Building 413 Chat Frontend",
        "mcp_config": "sustainable-eco-report-chatapp"
    })

if __name__ == '__main__':
    print("Starting Building 413 Chat Frontend...")
    print("MCP Server: http://localhost:4141/mcp")
    print("Using Ollama llama3.1 model")
    print("Frontend will be available at: http://localhost:5000")

    app.run(debug=True, host='0.0.0.0', port=5000) 