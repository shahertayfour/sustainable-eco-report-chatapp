import asyncio
import sys
from mcp_client import SustainableEcoMCPClient

async def test_mcp_integration():
    """Test MCP server and client integration."""
    
    print("=== Testing MCP Integration ===\n")
    
    # Initialize client with Ollama
    client = SustainableEcoMCPClient(llm_provider="ollama", model="llama3.1:8b")
    
    try:
        # Test 1: Connect to server
        print("Test 1: Connecting to MCP server...")
        await client.connect("mcp_server.py")
        print("✓ Connected successfully\n")
        
        # Test 2: Simple query
        print("Test 2: Simple energy query...")
        result = await client.query("What's the current total energy consumption?")
        print(f"Response: {result[:200]}..." if len(result) > 200 else f"Response: {result}")
        print("✓ Simple query successful\n")
        
        # Test 3: Tool chaining query
        print("Test 3: Tool chaining query...")
        result = await client.query(
            "Calculate the carbon footprint based on current energy consumption and provide recommendations"
        )
        print(f"Response: {result[:200]}..." if len(result) > 200 else f"Response: {result}")
        print("✓ Tool chaining successful\n")
        
        # Test 4: Period analysis
        print("Test 4: Period analysis...")
        result = await client.analyze_period("2024-01-01", "2024-01-31")
        print(f"Response: {result[:200]}..." if len(result) > 200 else f"Response: {result}")
        print("✓ Period analysis successful\n")
        
        # Test 5: Get recommendations
        print("Test 5: Get recommendations...")
        result = await client.get_recommendations()
        print(f"Response: {result[:200]}..." if len(result) > 200 else f"Response: {result}")
        print("✓ Recommendations retrieved successfully\n")
        
        print("=== All tests passed! ===")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
    
    return True

async def test_flask_integration():
    """Test Flask integration with MCP."""
    import requests
    import json
    
    print("\n=== Testing Flask MCP Integration ===\n")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test 1: Health check
        print("Test 1: Health check...")
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}, Response: {response.json()}")
        print("✓ Health check successful\n")
        
        # Test 2: Chat with sustainability query
        print("Test 2: Chat with sustainability query...")
        response = requests.post(
            f"{base_url}/chat",
            json={"message": "What's the building's energy consumption?"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"MCP Enabled: {data.get('mcp_enabled', False)}")
            print(f"Response: {data['message'][:200]}..." if len(data['message']) > 200 else f"Response: {data['message']}")
        print("✓ Chat endpoint successful\n")
        
        # Test 3: Analyze endpoint
        print("Test 3: Analyze endpoint - recommendations...")
        response = requests.post(
            f"{base_url}/analyze",
            json={"type": "recommendations"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data['result'][:200]}..." if len(data['result']) > 200 else f"Response: {data['result']}")
        print("✓ Analyze endpoint successful\n")
        
        # Test 4: Period analysis
        print("Test 4: Period analysis...")
        response = requests.post(
            f"{base_url}/analyze",
            json={
                "type": "period",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31"
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data['result'][:200]}..." if len(data['result']) > 200 else f"Response: {data['result']}")
        print("✓ Period analysis successful\n")
        
        print("=== Flask integration tests passed! ===")
        
    except Exception as e:
        print(f"✗ Flask test failed: {e}")
        print("Make sure the Flask app is running with: python app_with_mcp.py")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--flask":
        # Test Flask integration
        asyncio.run(test_flask_integration())
    else:
        # Test MCP client directly
        asyncio.run(test_mcp_integration())