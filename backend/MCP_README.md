# MCP Integration for Sustainable Eco Chat App

This project integrates Model Context Protocol (MCP) with the Sustainable Eco Chat application using FastMCP for the server and mcp-use for the client.

## Components

### 1. MCP Server (`mcp_server.py`)
- Built with FastMCP
- Provides three main tools:
  - `get_building_energy_stats`: Analyze energy consumption with date filtering
  - `analyze_eco_impact`: Calculate carbon footprint and water usage
  - `get_sustainability_metrics`: Get recommendations based on consumption
- Supports tool chaining for comprehensive analysis
- Includes prompts for sustainability reports and eco assistance

### 2. MCP Client (`mcp_client.py`)
- Uses mcp-use library for LLM integration
- Configured to use Ollama with llama3.1:8b model
- Supports multiple LLM providers (Ollama, OpenAI, Anthropic)
- Provides high-level methods for common queries:
  - `query()`: General queries with automatic tool selection
  - `analyze_period()`: Period-specific analysis
  - `get_recommendations()`: Sustainability recommendations
  - `compare_periods()`: Compare metrics between time periods

### 3. Flask Integration (`app_with_mcp.py`)
- Enhanced Flask backend with MCP capabilities
- Automatically routes sustainability queries to MCP
- Fallback to regular Ollama for non-sustainability queries
- New `/analyze` endpoint for structured analysis

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Ollama is running with llama3.1:8b model:
```bash
ollama pull llama3.1:8b
ollama serve
```

## Usage

### Running the MCP Server Standalone
```bash
python mcp_server.py
```

### Running the Flask App with MCP
```bash
python app_with_mcp.py
```

### Testing MCP Integration
```bash
# Test MCP client directly
python test_mcp.py

# Test Flask integration (run Flask app first)
python test_mcp.py --flask
```

## API Endpoints

### Enhanced Chat Endpoint
- **POST** `/chat`
- Automatically uses MCP for sustainability queries
- Request:
```json
{
  "message": "What's the building's carbon footprint?"
}
```
- Response includes `mcp_enabled` field

### Analysis Endpoint
- **POST** `/analyze`
- Types: `period`, `recommendations`, `compare`, or custom query
- Examples:

Period Analysis:
```json
{
  "type": "period",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

Recommendations:
```json
{
  "type": "recommendations"
}
```

Period Comparison:
```json
{
  "type": "compare",
  "period1_start": "2024-01-01",
  "period1_end": "2024-01-31",
  "period2_start": "2024-02-01",
  "period2_end": "2024-02-29"
}
```

## Tool Chaining Examples

The MCP tools are designed to work together:

1. **Complete Analysis Chain**:
   - Get energy stats → Calculate carbon footprint → Get recommendations

2. **Temporal Analysis**:
   - Get stats for specific period → Analyze impact → Compare with baseline

3. **Multi-metric Analysis**:
   - Analyze carbon footprint + water usage → Combined recommendations

## Environment Variables

Create a `.env` file with:
```
FLASK_PORT=5000
FLASK_DEBUG=False
# Optional for other LLM providers:
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## Architecture

```
User Query → Flask App → MCP Client → MCP Server → Tools → Data Analysis
                ↓                                               ↓
            Regular Ollama ←────── (fallback) ──────────── Results
```

## Troubleshooting

1. **MCP Connection Failed**: Ensure the MCP server script path is correct
2. **Ollama Not Found**: Check that Ollama is running on http://localhost:11434
3. **Tool Not Found**: Verify the FastMCP server is running with all tools registered
4. **Async Errors**: The Flask integration handles async/sync conversion automatically