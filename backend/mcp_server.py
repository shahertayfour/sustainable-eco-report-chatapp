from fastmcp import FastMCP
from typing import Optional
import pandas as pd
import os
import json
from datetime import datetime

mcp = FastMCP("sustainable-eco-chat")

DATASET_PATH = os.path.join(os.path.dirname(__file__), '../dataset/building_413_data.csv')

# Cache the dataset in memory for faster access
_DATASET_CACHE = None

def get_dataset():
    """Load and cache the dataset for faster access"""
    global _DATASET_CACHE
    if _DATASET_CACHE is None:
        print(f"Loading dataset from {DATASET_PATH}...")
        _DATASET_CACHE = pd.read_csv(DATASET_PATH)
        print(f"Dataset loaded: {len(_DATASET_CACHE)} records")
    return _DATASET_CACHE.copy()  # Return a copy to avoid modifying cache

@mcp.tool()
async def get_building_energy_stats(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """احصل على إحصائيات استهلاك الطاقة للمبنى ٤١٣

    تحليل أنماط استهلاك الطاقة مع إمكانية التسلسل مع أدوات أخرى للتحليل الشامل

    المعاملات:
        start_date: تاريخ البدء للتحليل (تنسيق YYYY-MM-DD)
        end_date: تاريخ الانتهاء للتحليل (تنسيق YYYY-MM-DD)

    Returns:
        JSON string with energy statistics including mean, max, min values in Arabic
    """
    try:
        df = get_dataset()

        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            if start_date:
                df = df[df['timestamp'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['timestamp'] <= pd.to_datetime(end_date)]

        # Translate column names to Arabic
        arabic_columns = {
            'datetime': 'التاريخ والوقت',
            'co2': 'ثاني أكسيد الكربون',
            'humidity': 'الرطوبة',
            'temperature': 'درجة الحرارة',
            'light': 'الإضاءة',
            'pir': 'كاشف الحركة',
            'building_id': 'رقم المبنى'
        }

        # Calculate statistics with Arabic labels
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        mean_dict = {}
        max_dict = {}
        min_dict = {}

        for col in numeric_df.columns:
            arabic_name = arabic_columns.get(col, col)
            # Convert numpy types to Python native types for JSON serialization
            mean_dict[arabic_name] = float(round(numeric_df[col].mean(), 2))
            max_dict[arabic_name] = float(round(numeric_df[col].max(), 2))
            min_dict[arabic_name] = float(round(numeric_df[col].min(), 2))

        stats = {
            "إجمالي_القراءات": int(len(df)),
            "المعايير_المراقبة": [arabic_columns.get(col, col) for col in df.columns.tolist()],
            "إحصائيات_استهلاك_الطاقة": {
                "المتوسط": mean_dict,
                "الحد_الأقصى": max_dict,
                "الحد_الأدنى": min_dict
            },
            "فترة_البيانات": {
                "من": str(df['datetime'].min()) if 'datetime' in df.columns else "غير متوفر",
                "إلى": str(df['datetime'].max()) if 'datetime' in df.columns else "غير متوفر"
            }
        }

        return json.dumps(stats, ensure_ascii=False)
    except Exception as e:
        return f"خطأ في قراءة بيانات المبنى: {str(e)}"

@mcp.tool()
async def get_sustainability_metrics() -> str:
    """احصل على مقاييس الاستدامة والتوصيات الحالية

    توفر هذه الأداة رؤى حول الاستدامة بناءً على أنماط استهلاك الطاقة ومصممة للعمل بالتسلسل مع أدوات التحليل الأخرى

    Returns:
        JSON string with sustainability metrics and recommendations in Arabic
    """
    try:
        df = get_dataset()

        energy_columns = [col for col in df.columns if 'energy' in col.lower() or 'power' in col.lower()]

        if energy_columns:
            total_energy = df[energy_columns].sum().sum()
            avg_energy = df[energy_columns].mean().mean()

            metrics = {
                "إجمالي_استهلاك_الطاقة": float(round(total_energy, 2)),
                "متوسط_استهلاك_الطاقة": float(round(avg_energy, 2)),
                "التوصيات": []
            }

            if avg_energy > 1000:
                metrics["التوصيات"].append("تم اكتشاف استهلاك عالي للطاقة. يُنصح بتطبيق تدابير توفير الطاقة.")
            if avg_energy > 500:
                metrics["التوصيات"].append("راقب أنماط استخدام الطاقة خلال ساعات الذروة.")
            else:
                metrics["التوصيات"].append("استهلاك الطاقة ضمن النطاقات الطبيعية.")
        else:
            # Fallback: analyze environmental data for sustainability insights
            co2_avg = df['co2'].mean() if 'co2' in df.columns else 0
            temp_avg = df['temperature'].mean() if 'temperature' in df.columns else 0
            humidity_avg = df['humidity'].mean() if 'humidity' in df.columns else 0
            light_avg = df['light'].mean() if 'light' in df.columns else 0
            pir_activity = (df['pir'].sum() / len(df) * 100) if 'pir' in df.columns else 0

            metrics = {
                "إجمالي_استهلاك_الطاقة": "لا يُقاس مباشرة",
                "متوسط_استهلاك_الطاقة": "مُقدّر من البيانات البيئية",
                "مستويات_ثاني_أكسيد_الكربون": f"{float(co2_avg):.1f} جزء في المليون",
                "متوسط_درجة_الحرارة": f"{float(temp_avg):.1f}°م",
                "متوسط_الرطوبة": f"{float(humidity_avg):.1f}٪",
                "متوسط_الإضاءة": f"{float(light_avg):.1f} لوكس",
                "نشاط_الحركة": f"{float(pir_activity):.1f}٪",
                "عدد_القراءات": int(len(df)),
                "التوصيات": []
            }

            if co2_avg > 1000:
                metrics["التوصيات"].append("مستويات ثاني أكسيد الكربون مرتفعة. حسّن أنظمة التهوية.")
            elif co2_avg > 600:
                metrics["التوصيات"].append("راقب مستويات ثاني أكسيد الكربون خلال ساعات الذروة.")

            if temp_avg > 25:
                metrics["التوصيات"].append("درجة الحرارة أعلى من النطاق الأمثل. انظر في تحسين نظام التبريد.")
            elif temp_avg < 22:
                metrics["التوصيات"].append("درجة الحرارة منخفضة. انظر في تحسين نظام التدفئة.")

            if humidity_avg > 60:
                metrics["التوصيات"].append("مستويات الرطوبة مرتفعة. انظر في إزالة الرطوبة.")
            elif humidity_avg < 40:
                metrics["التوصيات"].append("مستويات الرطوبة منخفضة. انظر في زيادة الترطيب.")

            if not metrics["التوصيات"]:
                metrics["التوصيات"].append("الظروف البيئية ضمن النطاقات المثلى.")

        return json.dumps(metrics, ensure_ascii=False)
    except Exception as e:
        return f"خطأ في حساب مقاييس الاستدامة: {str(e)}"

@mcp.tool()
async def analyze_eco_impact(metric_type: str = "carbon_footprint") -> str:
    """تحليل التأثير البيئي بناءً على بيانات المبنى

    تحسب هذه الأداة مقاييس التأثير البيئي وتتكامل بشكل جيد مع أدوات أخرى للتحليل الشامل للاستدامة

    Args:
        metric_type: نوع التأثير المراد تحليله ('carbon_footprint' للبصمة الكربونية أو 'water_usage' لاستخدام المياه)

    Returns:
        String with calculated environmental impact in Arabic
    """
    try:
        df = get_dataset()

        if metric_type == "carbon_footprint":
            # Estimate carbon footprint based on energy consumption patterns
            # Using CO2 levels and other environmental data as proxies

            if 'co2' in df.columns:
                avg_co2 = df['co2'].mean()
                max_co2 = df['co2'].max()
                min_co2 = df['co2'].min()
                co2_impact = avg_co2 * len(df) * 0.001  # Convert to kg CO2

                # Determine rating in Arabic
                if avg_co2 < 600:
                    rating = "ممتاز"
                    rating_desc = "جيد"
                elif avg_co2 < 1000:
                    rating = "يحتاج تحسين"
                    rating_desc = "مقبول"
                else:
                    rating = "ضعيف"
                    rating_desc = "يحتاج تحسين فوري"

                impact_analysis = {
                    "نوع_المقياس": "البصمة الكربونية",
                    "انبعاثات_CO2_المقدرة_كجم": float(round(co2_impact, 2)),
                    "متوسط_CO2_اليومي_جزء_بالمليون": float(round(avg_co2, 1)),
                    "الحد_الأقصى_CO2": float(round(max_co2, 1)),
                    "الحد_الأدنى_CO2": float(round(min_co2, 1)),
                    "تصنيف_الاستدامة": rating,
                    "وصف_التصنيف": rating_desc,
                    "عدد_القراءات": int(len(df)),
                    "التوصيات": []
                }

                if avg_co2 > 1000:
                    impact_analysis["التوصيات"].extend([
                        "تنفيذ تحسينات فورية للتهوية",
                        "النظر في مصادر الطاقة المتجددة",
                        "مراقبة أنماط الإشغال لتحسين نظام التدفئة والتهوية وتكييف الهواء"
                    ])
                elif avg_co2 > 600:
                    impact_analysis["التوصيات"].extend([
                        "مراقبة مستويات ثاني أكسيد الكربون خلال ساعات الذروة",
                        "تحسين جداول التهوية"
                    ])
                else:
                    impact_analysis["التوصيات"].append("الحفاظ على المعايير البيئية الحالية")

                return json.dumps(impact_analysis, ensure_ascii=False)

        elif metric_type == "water_usage":
            # Estimate water usage based on humidity and occupancy patterns
            if 'humidity' in df.columns and 'pir' in df.columns:
                avg_humidity = df['humidity'].mean()
                total_motion_events = df['pir'].sum()

                # Rough estimation based on occupancy and HVAC humidity control
                estimated_water_usage = (avg_humidity / 50) * total_motion_events * 10  # Liters

                # Determine efficiency rating in Arabic
                if 40 <= avg_humidity <= 60:
                    efficiency = "جيد"
                    efficiency_desc = "ضمن النطاق الأمثل"
                else:
                    efficiency = "يحتاج تحسين"
                    efficiency_desc = "خارج النطاق الأمثل"

                water_analysis = {
                    "نوع_المقياس": "استخدام المياه",
                    "الاستخدام_اليومي_المقدر_باللتر": float(round(estimated_water_usage, 2)),
                    "كفاءة_الرطوبة": efficiency,
                    "وصف_الكفاءة": efficiency_desc,
                    "متوسط_الرطوبة": f"{float(avg_humidity):.1f}٪",
                    "عامل_الإشغال": int(total_motion_events),
                    "عدد_القراءات": int(len(df)),
                    "التوصيات": []
                }

                if avg_humidity > 60:
                    water_analysis["التوصيات"].append("رطوبة عالية مكتشفة. تحقق من هدر المياه أو ضعف التهوية.")
                elif avg_humidity < 40:
                    water_analysis["التوصيات"].append("رطوبة منخفضة. انظر في استخدام المياه للترطيب.")
                else:
                    water_analysis["التوصيات"].append("مستويات الرطوبة مثالية.")

                return json.dumps(water_analysis, ensure_ascii=False)

        return f"تم إكمال التحليل لـ {metric_type} بالبيانات المتاحة."

    except Exception as e:
        return f"خطأ في تحليل التأثير البيئي: {str(e)}"

if __name__ == "__main__":
    # Run the MCP server with ASGI (web) transport on port 4141
    mcp.run()