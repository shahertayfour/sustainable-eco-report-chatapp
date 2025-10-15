"""HTTP server wrapper for the MCP server using uvicorn"""
import uvicorn
from fastmcp import FastMCP

# Import all tools from mcp_server
from mcp_server import (
    get_building_energy_stats,
    get_sustainability_metrics,
    analyze_eco_impact
)

# Create a new FastMCP instance with the same name
mcp_server = FastMCP("sustainable-eco-chat")

# Re-register all tools
mcp_server.add_tool(get_building_energy_stats)
mcp_server.add_tool(get_sustainability_metrics)
mcp_server.add_tool(analyze_eco_impact)

# Use the SSE app (Server-Sent Events) for HTTP transport
app = mcp_server.sse_app

if __name__ == "__main__":
    print("Starting MCP HTTP server on http://0.0.0.0:4141")
    print("MCP SSE endpoint: http://localhost:4141/sse")
    print("MCP available at: http://localhost:4141")
    # Use uvicorn to serve the MCP server
    uvicorn.run(app, host="0.0.0.0", port=4141, log_level="info")
