import asyncio
from typing import Optional, Dict, Any
from mcp_use import MCPAgent, MCPClient
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

class SustainableEcoMCPClient:
    """MCP Client for interacting with the Sustainable Eco Chat MCP Server using mcp-use.
    
    This client leverages the mcp-use library to connect any LLM to the FastMCP server,
    enabling tool chaining and comprehensive sustainability analysis.
    
    Example usage:
        # Create client with Ollama
        client = SustainableEcoMCPClient(llm_provider="ollama", model="llama3.1:8b")
        
        # Single query
        result = await client.query("What's the current energy consumption?")
        
        # Tool chaining query
        result = await client.query("Analyze last month's energy usage and calculate carbon footprint")
    """
    
    def __init__(self, llm_provider: str = "ollama", model: Optional[str] = None):
        """Initialize the MCP client with specified LLM provider.
        
        Args:
            llm_provider: LLM provider to use ("ollama", "openai", "anthropic")
            model: Specific model to use (optional, defaults to provider's default)
        """
        self.llm_provider = llm_provider
        self.llm = self._create_llm(llm_provider, model)
        self.client: Optional[MCPClient] = None
        self.agent: Optional[MCPAgent] = None
        
    def _create_llm(self, provider: str, model: Optional[str] = None):
        """Create LLM instance based on provider.
        
        Args:
            provider: LLM provider name
            model: Specific model name
            
        Returns:
            LLM instance
        """
        if provider == "ollama":
            return ChatOllama(
                model=model or "llama3.1:8b",
                temperature=0.7,
                base_url="http://localhost:11434"  # Default Ollama URL
            )
        elif provider == "openai":
            return ChatOpenAI(
                model=model or "gpt-4o",
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model or "claude-3-sonnet-20240229",
                temperature=0.7,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    async def connect(self, server_path: str = "mcp_server.py"):
        """Connect to the MCP server.
        
        Args:
            server_path: Path to the MCP server script
        """
        # Configuration for connecting to our FastMCP server
        config = {
            "mcpServers": {
                "sustainable-eco-chat": {
                    "command": "python",
                    "args": [server_path]
                }
            }
        }
        
        # Create MCP client from configuration
        self.client = MCPClient.from_dict(config)
        
        # Create MCP agent with tool access
        self.agent = MCPAgent(
            llm=self.llm,
            client=self.client,
            max_steps=10,  # Maximum tool calls in a chain
            system_prompt="""You are an AI assistant specialized in sustainable building management.
            
Your role is to analyze building data and provide sustainability insights using available tools:
- get_building_energy_stats: Get energy consumption statistics
- analyze_eco_impact: Calculate environmental impact (carbon footprint, water usage)
- get_sustainability_metrics: Get recommendations for improvement

When answering questions, use tool chaining for comprehensive analysis:
1. First gather relevant data using get_building_energy_stats
2. Then analyze impact using analyze_eco_impact
3. Finally get recommendations using get_sustainability_metrics

Always provide specific, actionable insights based on the data."""
        )
        
        print(f"Connected to MCP server using {self.llm_provider} ({self.llm.model})")
        
    async def query(self, prompt: str, stream: bool = False) -> str:
        """Send a query to the MCP agent.
        
        Args:
            prompt: The query to send
            stream: Whether to stream the response
            
        Returns:
            The agent's response
            
        Example queries that demonstrate tool chaining:
            - "What's our carbon footprint for January 2024?"
            - "Analyze energy consumption patterns and suggest improvements"
            - "Compare this month's sustainability metrics with last month"
        """
        if not self.agent:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        if stream:
            # Stream the response
            result = ""
            async for chunk in self.agent.stream(prompt):
                print(chunk, end="", flush=True)
                result += chunk
            return result
        else:
            # Get complete response
            return await self.agent.run(prompt)
    
    async def analyze_period(self, start_date: str, end_date: str) -> str:
        """Analyze sustainability metrics for a specific period.
        
        This method demonstrates programmatic tool chaining by constructing
        a prompt that will trigger multiple tool calls.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Comprehensive analysis results
        """
        prompt = f"""Perform a comprehensive sustainability analysis for the period {start_date} to {end_date}:
        1. Get energy statistics for this period
        2. Calculate the carbon footprint
        3. Analyze water usage if available
        4. Provide sustainability metrics and recommendations
        5. Suggest specific actions to improve sustainability"""
        
        return await self.query(prompt)
    
    async def get_recommendations(self) -> str:
        """Get current sustainability recommendations.
        
        This triggers a tool chain that analyzes current state and provides recommendations.
        
        Returns:
            Actionable sustainability recommendations
        """
        prompt = """Based on current building data:
        1. Analyze current energy consumption patterns
        2. Calculate environmental impact
        3. Provide specific recommendations for improvement
        4. Include estimated impact of each recommendation"""
        
        return await self.query(prompt)
    
    async def compare_periods(self, period1_start: str, period1_end: str, 
                            period2_start: str, period2_end: str) -> str:
        """Compare sustainability metrics between two periods.
        
        Args:
            period1_start: Start date of first period
            period1_end: End date of first period
            period2_start: Start date of second period
            period2_end: End date of second period
            
        Returns:
            Comparative analysis results
        """
        prompt = f"""Compare sustainability metrics between two periods:
        Period 1: {period1_start} to {period1_end}
        Period 2: {period2_start} to {period2_end}
        
        Analyze energy consumption, carbon footprint, and provide insights on improvements or regressions."""
        
        return await self.query(prompt)

# Example usage and testing
async def main():
    """Example demonstrating mcp-use client with Ollama llama3.1:8b model."""
    
    # Initialize client with Ollama llama3.1:8b
    client = SustainableEcoMCPClient(llm_provider="ollama", model="llama3.1:8b")
    
    try:
        # Connect to the FastMCP server
        await client.connect("mcp_server.py")
        
        print("\n--- Example 1: Simple Query ---")
        result = await client.query("What's the current energy consumption?")
        print(result)
        
        print("\n--- Example 2: Tool Chaining Query ---")
        result = await client.query(
            "Analyze the building's energy usage for the last 30 days and "
            "calculate the carbon footprint. Then provide recommendations."
        )
        print(result)
        
        print("\n--- Example 3: Period Analysis ---")
        result = await client.analyze_period("2024-01-01", "2024-01-31")
        print(result)
        
        print("\n--- Example 4: Streaming Response ---")
        print("Streaming analysis...")
        await client.query(
            "Give me a detailed sustainability report with all available metrics",
            stream=True
        )
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Run the example
    asyncio.run(main())