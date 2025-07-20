from fastmcp import FastMCP
from typing import Optional
import pandas as pd
import os
from datetime import datetime

mcp = FastMCP("sustainable-eco-chat")

DATASET_PATH = os.path.join(os.path.dirname(__file__), '../dataset/building_413_data.csv')

@mcp.tool()
async def get_building_energy_stats(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Get energy consumption statistics for Building 413.
    
    This tool analyzes energy consumption patterns and can be chained with other tools
    for comprehensive analysis.
    
    Args:
        start_date: Start date for analysis (YYYY-MM-DD format)
        end_date: End date for analysis (YYYY-MM-DD format)
    
    Returns:
        JSON string with energy statistics including mean, max, min values
    
    Example chaining:
        1. First call get_building_energy_stats() to get baseline data
        2. Then call analyze_eco_impact() to calculate carbon footprint
        3. Finally call get_sustainability_metrics() for recommendations
    
    Chain usage in prompts:
        "Analyze last month's energy usage and calculate the carbon impact"
        "Compare this week's energy stats with sustainability targets"
    """
    try:
        df = pd.read_csv(DATASET_PATH)
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            if start_date:
                df = df[df['timestamp'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['timestamp'] <= pd.to_datetime(end_date)]
        
        stats = {
            "total_records": len(df),
            "columns": df.columns.tolist(),
            "energy_consumption": {
                "mean": df.select_dtypes(include=['float64', 'int64']).mean().to_dict(),
                "max": df.select_dtypes(include=['float64', 'int64']).max().to_dict(),
                "min": df.select_dtypes(include=['float64', 'int64']).min().to_dict()
            }
        }
        
        return str(stats)
    except Exception as e:
        return f"Error reading building data: {str(e)}"

@mcp.tool()
async def get_sustainability_metrics() -> str:
    """Get current sustainability metrics and recommendations.
    
    This tool provides sustainability insights based on energy consumption patterns
    and is designed to work in chains with other analysis tools.
    
    Returns:
        JSON string with total/average energy consumption and recommendations
    
    Example chaining:
        1. get_building_energy_stats() → get_sustainability_metrics()
           Analyze patterns then get recommendations
        
        2. get_sustainability_metrics() → analyze_eco_impact('carbon_footprint')
           Get metrics then calculate environmental impact
    
    Chain usage in prompts:
        "Get sustainability metrics and create an action plan"
        "Analyze current metrics and suggest immediate improvements"
    """
    try:
        df = pd.read_csv(DATASET_PATH)
        
        energy_columns = [col for col in df.columns if 'energy' in col.lower() or 'power' in col.lower()]
        
        if energy_columns:
            total_energy = df[energy_columns].sum().sum()
            avg_energy = df[energy_columns].mean().mean()
            
            metrics = {
                "total_energy_consumption": total_energy,
                "average_energy_consumption": avg_energy,
                "recommendations": []
            }
            
            if avg_energy > 1000:
                metrics["recommendations"].append("High energy consumption detected. Consider implementing energy-saving measures.")
            if avg_energy > 500:
                metrics["recommendations"].append("Moderate energy usage. Look for opportunities to optimize during peak hours.")
            else:
                metrics["recommendations"].append("Energy consumption is within optimal range.")
                
            return str(metrics)
        else:
            return "No energy-related columns found in the dataset"
            
    except Exception as e:
        return f"Error calculating sustainability metrics: {str(e)}"

@mcp.tool()
async def analyze_eco_impact(
    metric_type: str = "carbon_footprint"
) -> str:
    """Analyze ecological impact based on building data.
    
    This tool calculates environmental impact metrics and integrates well with
    other tools for comprehensive sustainability analysis.
    
    Args:
        metric_type: Type of impact to analyze ('carbon_footprint' or 'water_usage')
    
    Returns:
        String with calculated environmental impact
    
    Example chaining:
        1. Complete analysis chain:
           get_building_energy_stats() → analyze_eco_impact() → get_sustainability_metrics()
           
        2. Impact comparison chain:
           analyze_eco_impact('carbon_footprint') + analyze_eco_impact('water_usage')
           
        3. Temporal analysis chain:
           get_building_energy_stats(start_date='2024-01-01') → analyze_eco_impact()
    
    Chain usage in prompts:
        "Calculate this month's carbon footprint and compare with targets"
        "Analyze both water and energy impact, then suggest improvements"
    """
    try:
        df = pd.read_csv(DATASET_PATH)
        
        if metric_type == "carbon_footprint":
            energy_columns = [col for col in df.columns if 'energy' in col.lower()]
            if energy_columns:
                total_energy_kwh = df[energy_columns].sum().sum()
                carbon_emissions_kg = total_energy_kwh * 0.5  # Approximate CO2 per kWh
                
                return f"Estimated carbon footprint: {carbon_emissions_kg:.2f} kg CO2"
        
        elif metric_type == "water_usage":
            water_columns = [col for col in df.columns if 'water' in col.lower()]
            if water_columns:
                total_water = df[water_columns].sum().sum()
                return f"Total water usage: {total_water:.2f} liters"
            else:
                return "No water usage data available"
                
        else:
            return f"Unknown metric type: {metric_type}"
            
    except Exception as e:
        return f"Error analyzing eco impact: {str(e)}"

@mcp.prompt()
async def sustainability_report_prompt() -> str:
    """Generate a comprehensive sustainability report.
    
    This prompt template uses tool chaining to create detailed reports:
    1. Gathers energy statistics
    2. Analyzes environmental impact
    3. Generates recommendations
    
    Example usage:
        "Use the sustainability report prompt to analyze Q1 2024"
        "Generate a report focusing on carbon reduction opportunities"
    """
    return """You are an expert sustainability consultant analyzing building data.
    
Please provide a comprehensive sustainability report that includes:
1. Current energy consumption patterns
2. Environmental impact assessment
3. Specific recommendations for improvement
4. Cost-benefit analysis of proposed changes
5. Timeline for implementation

Use the available tools to gather building data and metrics.

Tool chaining approach:
- Start with get_building_energy_stats() for baseline data
- Use analyze_eco_impact() for environmental metrics
- Apply get_sustainability_metrics() for recommendations
- Combine insights for comprehensive analysis"""

@mcp.prompt()
async def eco_assistant_prompt() -> str:
    """Act as an eco-friendly building assistant.
    
    This prompt enables intelligent tool chaining for sustainability queries:
    - Automatically determines which tools to use based on the question
    - Chains multiple tools for comprehensive answers
    - Provides actionable insights based on data
    
    Example usage:
        "How can we reduce our carbon footprint this quarter?"
        "What's our current sustainability score and how to improve it?"
    """
    return """You are an AI assistant specialized in sustainable building management.
    
Your role is to:
- Monitor and analyze building energy consumption
- Provide actionable sustainability recommendations
- Calculate environmental impact metrics
- Suggest eco-friendly alternatives
- Help achieve carbon neutrality goals

Always base your responses on actual building data when available.

Tool chaining strategy:
1. For general queries: get_sustainability_metrics() first
2. For specific periods: get_building_energy_stats(dates) → analyze_eco_impact()
3. For comprehensive analysis: chain all three tools in sequence
4. Always end with actionable recommendations"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp_server:mcp", host="0.0.0.0", port=8000, reload=True)