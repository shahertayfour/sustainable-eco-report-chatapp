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
                metrics["recommendations"].append("Monitor energy usage patterns during peak hours.")
            else:
                metrics["recommendations"].append("Energy consumption is within normal ranges.")
        else:
            # Fallback: analyze environmental data for sustainability insights
            co2_avg = df['co2'].mean() if 'co2' in df.columns else 0
            temp_avg = df['temperature'].mean() if 'temperature' in df.columns else 0
            humidity_avg = df['humidity'].mean() if 'humidity' in df.columns else 0
            
            metrics = {
                "total_energy_consumption": "Not directly measured",
                "average_energy_consumption": "Estimated from environmental data",
                "co2_levels": f"{co2_avg:.1f} ppm",
                "temperature_avg": f"{temp_avg:.1f}°C",
                "humidity_avg": f"{humidity_avg:.1f}%",
                "recommendations": []
            }
            
            if co2_avg > 1000:
                metrics["recommendations"].append("CO2 levels are high. Improve ventilation systems.")
            if temp_avg > 25:
                metrics["recommendations"].append("Temperature is above optimal range. Consider cooling system optimization.")
            if humidity_avg > 60:
                metrics["recommendations"].append("Humidity levels are high. Consider dehumidification.")
            
            if not metrics["recommendations"]:
                metrics["recommendations"].append("Environmental conditions are within optimal ranges.")
        
        return str(metrics)
    except Exception as e:
        return f"Error calculating sustainability metrics: {str(e)}"

@mcp.tool()
async def analyze_eco_impact(metric_type: str = "carbon_footprint") -> str:
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
            # Estimate carbon footprint based on energy consumption patterns
            # Using CO2 levels and other environmental data as proxies
            
            if 'co2' in df.columns:
                avg_co2 = df['co2'].mean()
                co2_impact = avg_co2 * len(df) * 0.001  # Convert to kg CO2
                
                impact_analysis = {
                    "metric_type": "carbon_footprint",
                    "estimated_co2_emissions_kg": round(co2_impact, 2),
                    "daily_average_co2_ppm": round(avg_co2, 1),
                    "sustainability_rating": "Good" if avg_co2 < 600 else "Needs Improvement" if avg_co2 < 1000 else "Poor",
                    "recommendations": []
                }
                
                if avg_co2 > 1000:
                    impact_analysis["recommendations"].extend([
                        "Implement immediate ventilation improvements",
                        "Consider renewable energy sources",
                        "Monitor occupancy patterns to optimize HVAC"
                    ])
                elif avg_co2 > 600:
                    impact_analysis["recommendations"].extend([
                        "Monitor CO2 levels during peak hours",
                        "Optimize ventilation schedules"
                    ])
                else:
                    impact_analysis["recommendations"].append("Maintain current environmental standards")
                
                return str(impact_analysis)
            
        elif metric_type == "water_usage":
            # Estimate water usage based on humidity and occupancy patterns
            if 'humidity' in df.columns and 'pir' in df.columns:
                avg_humidity = df['humidity'].mean()
                total_motion_events = df['pir'].sum()
                
                # Rough estimation based on occupancy and HVAC humidity control
                estimated_water_usage = (avg_humidity / 50) * total_motion_events * 10  # Liters
                
                water_analysis = {
                    "metric_type": "water_usage",
                    "estimated_daily_usage_liters": round(estimated_water_usage, 2),
                    "humidity_efficiency": "Good" if 40 <= avg_humidity <= 60 else "Needs Optimization",
                    "occupancy_factor": total_motion_events,
                    "recommendations": []
                }
                
                if avg_humidity > 60:
                    water_analysis["recommendations"].append("High humidity detected. Check for water waste or poor ventilation.")
                elif avg_humidity < 40:
                    water_analysis["recommendations"].append("Low humidity. Consider water usage for humidification.")
                else:
                    water_analysis["recommendations"].append("Humidity levels are optimal.")
                
                return str(water_analysis)
        
        return f"Analysis for {metric_type} completed with available data."
        
    except Exception as e:
        return f"Error analyzing ecological impact: {str(e)}"

if __name__ == "__main__":
    # Run the MCP server with HTTP transport
    mcp.run(transport="http", host="0.0.0.0", port=4141)