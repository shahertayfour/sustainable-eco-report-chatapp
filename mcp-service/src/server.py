#!/usr/bin/env python3
"""
MCP Server for Sustainable Smart Home Data Analysis
Uses fastmcp to provide data analysis tools for building sensor data
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
import json

from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Smart Home Data Server")

# Global variables for data storage
building_data: Optional[pd.DataFrame] = None
data_loaded = False

def load_dataset():
    """Load the building sensor data"""
    global building_data, data_loaded
    
    if data_loaded:
        return
    
    try:
        dataset_path = Path(__file__).parent.parent.parent / "dataset" / "building_413_data.csv"
        building_data = pd.read_csv(dataset_path)
        building_data['datetime'] = pd.to_datetime(building_data['datetime'])
        building_data = building_data.sort_values('datetime')
        data_loaded = True
        print(f"Loaded {len(building_data)} records from building sensor data")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        building_data = pd.DataFrame()

@mcp.tool()
def get_data_summary() -> str:
    """Get a summary of the available building sensor data"""
    load_dataset()
    
    if building_data.empty:
        return "No data available"
    
    summary = {
        "total_records": len(building_data),
        "date_range": {
            "start": building_data['datetime'].min().isoformat(),
            "end": building_data['datetime'].max().isoformat()
        },
        "building_id": building_data['building_id'].iloc[0],
        "sensors": {
            "co2": {
                "available_records": building_data['co2'].notna().sum(),
                "avg_value": round(building_data['co2'].mean(), 2) if building_data['co2'].notna().any() else None,
                "min_value": round(building_data['co2'].min(), 2) if building_data['co2'].notna().any() else None,
                "max_value": round(building_data['co2'].max(), 2) if building_data['co2'].notna().any() else None
            },
            "temperature": {
                "available_records": building_data['temperature'].notna().sum(),
                "avg_value": round(building_data['temperature'].mean(), 2) if building_data['temperature'].notna().any() else None,
                "min_value": round(building_data['temperature'].min(), 2) if building_data['temperature'].notna().any() else None,
                "max_value": round(building_data['temperature'].max(), 2) if building_data['temperature'].notna().any() else None
            },
            "humidity": {
                "available_records": building_data['humidity'].notna().sum(),
                "avg_value": round(building_data['humidity'].mean(), 2) if building_data['humidity'].notna().any() else None,
                "min_value": round(building_data['humidity'].min(), 2) if building_data['humidity'].notna().any() else None,
                "max_value": round(building_data['humidity'].max(), 2) if building_data['humidity'].notna().any() else None
            },
            "light": {
                "available_records": building_data['light'].notna().sum(),
                "avg_value": round(building_data['light'].mean(), 2) if building_data['light'].notna().any() else None,
                "min_value": round(building_data['light'].min(), 2) if building_data['light'].notna().any() else None,
                "max_value": round(building_data['light'].max(), 2) if building_data['light'].notna().any() else None
            },
            "pir_motion": {
                "available_records": building_data['pir'].notna().sum(),
                "total_motion_events": int(building_data['pir'].sum()) if building_data['pir'].notna().any() else 0
            }
        }
    }
    
    return json.dumps(summary, indent=2)

@mcp.tool()
def analyze_co2_levels(start_date: str = "", end_date: str = "") -> str:
    """Analyze CO2 levels for sustainability insights
    
    Args:
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    """
    load_dataset()
    
    if building_data.empty:
        return "No data available"
    
    df = building_data.copy()
    
    # Filter by date range if provided
    if start_date:
        df = df[df['datetime'] >= start_date]
    if end_date:
        df = df[df['datetime'] <= end_date]
    
    co2_data = df['co2'].dropna()
    
    if co2_data.empty:
        return "No CO2 data available for the specified period"
    
    # CO2 level categories (ppm)
    excellent = (co2_data <= 400).sum()
    good = ((co2_data > 400) & (co2_data <= 600)).sum()
    acceptable = ((co2_data > 600) & (co2_data <= 1000)).sum()
    poor = ((co2_data > 1000) & (co2_data <= 1500)).sum()
    very_poor = (co2_data > 1500).sum()
    
    analysis = {
        "period": {
            "start": df['datetime'].min().isoformat(),
            "end": df['datetime'].max().isoformat(),
            "total_readings": len(co2_data)
        },
        "co2_statistics": {
            "average_ppm": round(co2_data.mean(), 2),
            "median_ppm": round(co2_data.median(), 2),
            "min_ppm": round(co2_data.min(), 2),
            "max_ppm": round(co2_data.max(), 2),
            "std_ppm": round(co2_data.std(), 2)
        },
        "air_quality_distribution": {
            "excellent_0_400ppm": {"count": excellent, "percentage": round(excellent/len(co2_data)*100, 1)},
            "good_400_600ppm": {"count": good, "percentage": round(good/len(co2_data)*100, 1)},
            "acceptable_600_1000ppm": {"count": acceptable, "percentage": round(acceptable/len(co2_data)*100, 1)},
            "poor_1000_1500ppm": {"count": poor, "percentage": round(poor/len(co2_data)*100, 1)},
            "very_poor_1500plus_ppm": {"count": very_poor, "percentage": round(very_poor/len(co2_data)*100, 1)}
        },
        "sustainability_insights": {
            "overall_rating": "excellent" if co2_data.mean() <= 400 else 
                            "good" if co2_data.mean() <= 600 else
                            "acceptable" if co2_data.mean() <= 1000 else
                            "poor" if co2_data.mean() <= 1500 else "very_poor",
            "ventilation_needed": co2_data.mean() > 1000,
            "energy_efficiency_score": max(0, 100 - (co2_data.mean() - 400) / 10)
        }
    }
    
    return json.dumps(analysis, indent=2)

@mcp.tool()
def analyze_occupancy_patterns() -> str:
    """Analyze occupancy patterns using PIR motion sensor data"""
    load_dataset()
    
    if building_data.empty:
        return "No data available"
    
    df = building_data.copy()
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.day_name()
    
    pir_data = df[df['pir'].notna()].copy()
    
    if pir_data.empty:
        return "No motion sensor data available"
    
    # Analyze patterns
    hourly_activity = pir_data.groupby('hour')['pir'].sum().to_dict()
    daily_activity = pir_data.groupby('day_of_week')['pir'].sum().to_dict()
    
    total_motion_events = int(pir_data['pir'].sum())
    peak_hour = max(hourly_activity, key=hourly_activity.get)
    peak_day = max(daily_activity, key=daily_activity.get)
    
    analysis = {
        "occupancy_summary": {
            "total_motion_events": total_motion_events,
            "monitoring_period": {
                "start": pir_data['datetime'].min().isoformat(),
                "end": pir_data['datetime'].max().isoformat()
            },
            "peak_activity_hour": peak_hour,
            "peak_activity_day": peak_day
        },
        "hourly_pattern": hourly_activity,
        "daily_pattern": daily_activity,
        "energy_optimization_insights": {
            "high_usage_hours": [hour for hour, count in hourly_activity.items() if count > np.mean(list(hourly_activity.values()))],
            "low_usage_hours": [hour for hour, count in hourly_activity.items() if count < np.mean(list(hourly_activity.values())) * 0.5],
            "recommendations": [
                "Reduce HVAC during low occupancy hours",
                "Optimize lighting schedules based on motion patterns",
                "Consider automated systems for peak usage times"
            ]
        }
    }
    
    return json.dumps(analysis, indent=2)

@mcp.tool()
def get_environmental_comfort_analysis() -> str:
    """Analyze temperature and humidity for optimal comfort and energy efficiency"""
    load_dataset()
    
    if building_data.empty:
        return "No data available"
    
    df = building_data.copy()
    temp_data = df['temperature'].dropna()
    humidity_data = df['humidity'].dropna()
    
    if temp_data.empty and humidity_data.empty:
        return "No temperature or humidity data available"
    
    analysis = {
        "temperature_analysis": {},
        "humidity_analysis": {},
        "comfort_insights": {}
    }
    
    if not temp_data.empty:
        # Optimal temperature range: 20-24°C
        optimal_temp = ((temp_data >= 20) & (temp_data <= 24)).sum()
        analysis["temperature_analysis"] = {
            "average_celsius": round(temp_data.mean(), 2),
            "min_celsius": round(temp_data.min(), 2),
            "max_celsius": round(temp_data.max(), 2),
            "optimal_range_20_24c": {
                "count": optimal_temp,
                "percentage": round(optimal_temp/len(temp_data)*100, 1)
            },
            "too_cold_below_20c": ((temp_data < 20).sum()),
            "too_warm_above_24c": ((temp_data > 24).sum())
        }
    
    if not humidity_data.empty:
        # Optimal humidity range: 40-60%
        optimal_humidity = ((humidity_data >= 40) & (humidity_data <= 60)).sum()
        analysis["humidity_analysis"] = {
            "average_percent": round(humidity_data.mean(), 2),
            "min_percent": round(humidity_data.min(), 2),
            "max_percent": round(humidity_data.max(), 2),
            "optimal_range_40_60": {
                "count": optimal_humidity,
                "percentage": round(optimal_humidity/len(humidity_data)*100, 1)
            },
            "too_dry_below_40": ((humidity_data < 40).sum()),
            "too_humid_above_60": ((humidity_data > 60).sum())
        }
    
    # Combined comfort analysis
    if not temp_data.empty and not humidity_data.empty:
        # Find records with both temp and humidity data
        combined_data = df[df['temperature'].notna() & df['humidity'].notna()]
        if not combined_data.empty:
            comfort_count = len(combined_data[
                (combined_data['temperature'] >= 20) & (combined_data['temperature'] <= 24) &
                (combined_data['humidity'] >= 40) & (combined_data['humidity'] <= 60)
            ])
            analysis["comfort_insights"] = {
                "optimal_comfort_conditions": {
                    "count": comfort_count,
                    "percentage": round(comfort_count/len(combined_data)*100, 1)
                },
                "energy_efficiency_score": min(100, comfort_count/len(combined_data)*100 + 20),
                "recommendations": [
                    "Maintain temperature between 20-24°C for optimal comfort",
                    "Keep humidity between 40-60% to prevent mold and dryness",
                    "Use smart thermostats to optimize energy usage"
                ]
            }
    
    return json.dumps(analysis, indent=2)

@mcp.tool()
def generate_sustainability_report(report_type: str = "comprehensive") -> str:
    """Generate a comprehensive sustainability report
    
    Args:
        report_type: Type of report ('comprehensive', 'co2_focused', 'energy_efficiency')
    """
    load_dataset()
    
    if building_data.empty:
        return "No data available for report generation"
    
    # Get all analysis data
    co2_analysis = json.loads(analyze_co2_levels())
    occupancy_analysis = json.loads(analyze_occupancy_patterns())
    comfort_analysis = json.loads(get_environmental_comfort_analysis())
    data_summary = json.loads(get_data_summary())
    
    report = {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "report_type": report_type,
            "building_id": data_summary.get("building_id"),
            "analysis_period": data_summary.get("date_range")
        },
        "executive_summary": {
            "total_records_analyzed": data_summary.get("total_records"),
            "overall_sustainability_score": 0,
            "key_findings": [],
            "priority_recommendations": []
        },
        "detailed_analysis": {
            "air_quality": co2_analysis,
            "occupancy_patterns": occupancy_analysis,
            "environmental_comfort": comfort_analysis
        },
        "sustainability_metrics": {},
        "recommendations": []
    }
    
    # Calculate overall sustainability score
    scores = []
    if "sustainability_insights" in co2_analysis:
        scores.append(co2_analysis["sustainability_insights"].get("energy_efficiency_score", 50))
    if "comfort_insights" in comfort_analysis:
        scores.append(comfort_analysis["comfort_insights"].get("energy_efficiency_score", 50))
    
    overall_score = round(np.mean(scores), 1) if scores else 50
    report["executive_summary"]["overall_sustainability_score"] = overall_score
    
    # Key findings
    findings = []
    if co2_analysis.get("co2_statistics", {}).get("average_ppm", 0) > 1000:
        findings.append("CO2 levels indicate poor ventilation - immediate action needed")
    if comfort_analysis.get("comfort_insights", {}).get("optimal_comfort_conditions", {}).get("percentage", 0) < 50:
        findings.append("Environmental conditions are suboptimal for comfort and efficiency")
    
    report["executive_summary"]["key_findings"] = findings
    
    # Recommendations based on analysis
    recommendations = []
    if co2_analysis.get("sustainability_insights", {}).get("ventilation_needed", False):
        recommendations.append("Improve ventilation system to reduce CO2 levels")
    
    if occupancy_analysis.get("energy_optimization_insights"):
        recommendations.extend(occupancy_analysis["energy_optimization_insights"].get("recommendations", []))
    
    if comfort_analysis.get("comfort_insights", {}).get("recommendations"):
        recommendations.extend(comfort_analysis["comfort_insights"]["recommendations"])
    
    report["recommendations"] = recommendations
    report["executive_summary"]["priority_recommendations"] = recommendations[:3]
    
    return json.dumps(report, indent=2)

if __name__ == "__main__":
    print("Starting Smart Home Data MCP Server...")
    print("Available tools:")
    print("- get_data_summary: Get overview of available sensor data")
    print("- analyze_co2_levels: Analyze air quality and CO2 levels")
    print("- analyze_occupancy_patterns: Analyze motion sensor data for occupancy patterns")
    print("- get_environmental_comfort_analysis: Analyze temperature and humidity")
    print("- generate_sustainability_report: Generate comprehensive sustainability reports")
    
    # Load data on startup
    load_dataset()
    
    # Run the server
    mcp.run()