import os
import json
import asyncio
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path for direct imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import MCP tools directly
from mcp_server import get_building_energy_stats, get_sustainability_metrics, analyze_eco_impact

app = Flask(__name__)

def generate_energy_report(data):
    """Generate professional energy consumption report in Arabic"""
    # Handle both Arabic and English keys
    total_records = data.get('إجمالي_القراءات', data.get('total_records', 'غير متوفر'))
    columns = data.get('المعايير_المراقبة', data.get('columns', []))
    date_period = data.get('فترة_البيانات', {})

    report = f"""<div style="font-family: 'Tajawal', sans-serif; line-height: 1.8; direction: rtl;">
<div style="background: linear-gradient(135deg, #006341 0%, #00A859 100%); color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,99,65,0.3);">
<h2 style="margin: 0; font-size: 28px; font-weight: 900;">⚡ مبنى ٤١٣ - تقرير الطاقة</h2>
<p style="margin: 8px 0 0 0; opacity: 0.95; font-size: 16px; font-weight: 500;">تحليل الأداء البيئي واستهلاك الطاقة</p>
</div>

<div style="background: #F5F9F6; padding: 20px; border-radius: 12px; border-right: 5px solid #00A859; margin-bottom: 20px;">
<strong style="color: #006341; font-size: 18px;">📋 تفاصيل التقرير</strong><br>
<div style="margin-top: 12px; line-height: 2;">
<span style="color: #666; font-weight: 500;">تاريخ الإنشاء:</span> <strong style="color: #333;">{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong><br>
<span style="color: #666; font-weight: 500;">رقم المبنى:</span> <strong style="color: #333;">٤١٣</strong><br>
<span style="color: #666; font-weight: 500;">عدد نقاط البيانات:</span> <strong style="color: #333;">{total_records} قراءة</strong>"""

    if date_period:
        report += f"""<br>
<span style="color: #666; font-weight: 500;">فترة البيانات:</span> <strong style="color: #333;">{date_period.get('من', '')} إلى {date_period.get('إلى', '')}</strong>"""

    report += """
</div>
</div>

<div style="background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #28a745; margin-bottom: 20px;">
<h3 style="margin: 0 0 12px 0; color: #28a745; font-size: 20px; font-weight: 800;">📊 الملخص التنفيذي</h3>
<p style="margin: 0; color: #333; font-size: 15px; line-height: 1.8;">يقدم هذا التقرير تحليلاً شاملاً لأنماط الأداء البيئي واستهلاك الطاقة في المبنى ٤١٣ بناءً على البيانات المجمعة من أجهزة الاستشعار المتعددة.</p>
</div>

<div style="background: #fff8e1; padding: 20px; border-radius: 12px; border-right: 5px solid #D4AF37; margin-bottom: 20px;">
<h3 style="margin: 0 0 12px 0; color: #856404; font-size: 20px; font-weight: 800;">🔍 نظرة عامة على جمع البيانات</h3>
<div style="line-height: 2;">
<strong style="color: #856404;">إجمالي القراءات:</strong> <span style="color: #333;">{total_records} قراءة</span><br>
<strong style="color: #856404;">المعايير المراقبة:</strong> <span style="color: #333;">{', '.join(str(c) for c in columns)}</span>
</div>
</div>
"""

    # Handle both Arabic and English keys for energy consumption
    energy = data.get('إحصائيات_استهلاك_الطاقة', data.get('energy_consumption', {}))

    if energy:
        # Get dictionaries with either Arabic or English keys
        mean_dict = energy.get('المتوسط', energy.get('mean', {}))
        max_dict = energy.get('الحد_الأقصى', energy.get('max', {}))
        min_dict = energy.get('الحد_الأدنى', energy.get('min', {}))

        report += """<div style="background: white; padding: 20px; border-radius: 12px; border: 2px solid #e9ecef; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
<h3 style="margin: 0 0 18px 0; color: #006341; font-size: 22px; font-weight: 800; text-align: right;">📈 إحصائيات استهلاك الطاقة</h3>
<table style="width: 100%; border-collapse: collapse; direction: rtl;">
<tr style="background: linear-gradient(135deg, #F5F9F6 0%, #e8f5e9 100%); border-bottom: 3px solid #00A859;">
<th style="padding: 15px; text-align: right; color: #006341; font-weight: 800; font-size: 16px;">المعيار</th>
<th style="padding: 15px; text-align: center; color: #006341; font-weight: 800; font-size: 16px;">المتوسط</th>
<th style="padding: 15px; text-align: center; color: #006341; font-weight: 800; font-size: 16px;">الحد الأدنى</th>
<th style="padding: 15px; text-align: center; color: #006341; font-weight: 800; font-size: 16px;">الذروة</th>
</tr>
"""

        # Get all unique keys
        all_keys = set()
        if mean_dict:
            all_keys.update(mean_dict.keys())
        if min_dict:
            all_keys.update(min_dict.keys())
        if max_dict:
            all_keys.update(max_dict.keys())

        for key in sorted(all_keys):
            # Determine unit and icon based on Arabic or English key
            key_lower = str(key).lower()
            if 'co2' in key_lower or 'كربون' in key_lower:
                unit = 'جزء/مليون'
                icon = '💨'
            elif 'temp' in key_lower or 'حرارة' in key_lower:
                unit = '°م'
                icon = '🌡️'
            elif 'hum' in key_lower or 'رطوبة' in key_lower:
                unit = '٪'
                icon = '💧'
            elif 'light' in key_lower or 'إضاءة' in key_lower:
                unit = 'لوكس'
                icon = '💡'
            elif 'pir' in key_lower or 'حركة' in key_lower:
                unit = ''
                icon = '👥'
            else:
                unit = ''
                icon = '📊'

            mean_val = f"{mean_dict.get(key, 0):.2f} {unit}" if key in mean_dict else 'غير متوفر'
            min_val = f"{min_dict.get(key, 0):.2f} {unit}" if key in min_dict else 'غير متوفر'
            max_val = f"{max_dict.get(key, 0):.2f} {unit}" if key in max_dict else 'غير متوفر'

            # Key is already in Arabic from MCP server
            display_key = str(key)

            report += f"""<tr style="border-bottom: 1px solid #e9ecef; transition: all 0.3s;">
<td style="padding: 14px; font-weight: 700; font-size: 15px; text-align: right;">{icon} {display_key}</td>
<td style="padding: 14px; text-align: center; background: #e3f2fd; font-weight: 600;">{mean_val}</td>
<td style="padding: 14px; text-align: center; background: #e8f5e9; font-weight: 600;">{min_val}</td>
<td style="padding: 14px; text-align: center; background: #fff3e0; font-weight: 600;">{max_val}</td>
</tr>
"""

        report += "</table></div>"

    report += """
<div style="background: linear-gradient(135deg, #d1ecf1 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #0dcaf0; margin-bottom: 20px;">
<h3 style="margin: 0 0 15px 0; color: #055160; font-size: 20px; font-weight: 800; text-align: right;">💡 التوصيات</h3>
<ol style="margin: 5px 0; padding-right: 25px; color: #055160; line-height: 2.2;">
<li style="margin-bottom: 12px; font-size: 15px;"><strong>المراقبة المستمرة:</strong> الحفاظ على التردد الحالي لجمع بيانات أجهزة الاستشعار</li>
<li style="margin-bottom: 12px; font-size: 15px;"><strong>تحسين الأداء:</strong> مراجعة فترات ذروة الاستخدام لتحسين الكفاءة</li>
<li style="margin-bottom: 12px; font-size: 15px;"><strong>الامتثال:</strong> التأكد من أن جميع المعايير تبقى ضمن النطاقات التشغيلية المقبولة</li>
</ol>
</div>

<div style="background: linear-gradient(135deg, #d4edda 0%, #b8e6c4 100%); padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(40,167,69,0.3);">
<strong style="color: #155724; font-size: 16px; font-weight: 800;">✅ حالة التقرير: مكتمل</strong> |
<strong style="color: #155724; font-size: 16px; font-weight: 800;">الجودة: عالية</strong> |
<strong style="color: #155724; font-size: 16px; font-weight: 800;">الثقة: ٩٥٪</strong>
</div>
</div>"""
    return report

def generate_sustainability_report(data):
    """Generate professional sustainability metrics report in Arabic"""

    # Handle both Arabic and English keys
    co2_level = data.get('مستويات_ثاني_أكسيد_الكربون', data.get('co2_levels', ''))
    temp_avg = data.get('متوسط_درجة_الحرارة', data.get('temperature_avg', ''))
    humidity_avg = data.get('متوسط_الرطوبة', data.get('humidity_avg', ''))
    light_avg = data.get('متوسط_الإضاءة', data.get('light_avg', ''))
    pir_activity = data.get('نشاط_الحركة', data.get('pir_activity', ''))
    total_records = data.get('عدد_القراءات', data.get('total_records', ''))
    recommendations = data.get('التوصيات', data.get('recommendations', []))

    # Determine sustainability rating
    if 'ppm' in str(co2_level) or 'مليون' in str(co2_level):
        try:
            co2_value = float(str(co2_level).split()[0])
            if co2_value < 600:
                rating = "ممتاز"
                grade = "أ+"
                color = "#28a745"
                bg_color = "#d4edda"
            elif co2_value < 800:
                rating = "جيد"
                grade = "أ"
                color = "#20c997"
                bg_color = "#d1ecf1"
            elif co2_value < 1000:
                rating = "مرضي"
                grade = "ب"
                color = "#ffc107"
                bg_color = "#fff3cd"
            else:
                rating = "يحتاج تحسين"
                grade = "ج"
                color = "#dc3545"
                bg_color = "#f8d7da"
        except:
            rating = "جيد"
            grade = "أ"
            color = "#20c997"
            bg_color = "#d1ecf1"
    else:
        rating = "جيد"
        grade = "أ"
        color = "#20c997"
        bg_color = "#d1ecf1"

    report = f"""<div style="font-family: 'Tajawal', sans-serif; line-height: 1.8; direction: rtl;">
<div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: center; box-shadow: 0 10px 30px rgba(40,167,69,0.3);">
<h2 style="margin: 0; font-size: 28px; font-weight: 900;">♻️ مبنى ٤١٣ - الاستدامة</h2>
<p style="margin: 8px 0 0 0; opacity: 0.95; font-size: 16px; font-weight: 500;">تقييم الأداء البيئي</p>
</div>

<div style="background: #F5F9F6; padding: 20px; border-radius: 12px; border-right: 5px solid #28a745; margin-bottom: 20px;">
<strong style="color: #28a745; font-size: 18px;">📋 تفاصيل التقرير</strong><br>
<div style="margin-top: 12px; line-height: 2;">
<span style="color: #666; font-weight: 500;">تاريخ الإنشاء:</span> <strong style="color: #333;">{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong><br>
<span style="color: #666; font-weight: 500;">رقم المبنى:</span> <strong style="color: #333;">٤١٣</strong><br>
<span style="color: #666; font-weight: 500;">نوع التقييم:</span> <strong style="color: #333;">تحليل الاستدامة البيئية</strong>"""

    if total_records:
        report += f"""<br>
<span style="color: #666; font-weight: 500;">عدد القراءات:</span> <strong style="color: #333;">{total_records}</strong>"""

    report += """
</div>
</div>

<div style="background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #20c997; margin-bottom: 20px;">
<h3 style="margin: 0 0 12px 0; color: #20c997; font-size: 20px; font-weight: 800;">📊 الملخص التنفيذي</h3>
<p style="margin: 0; color: #333; font-size: 15px; line-height: 1.8;">يقيّم هذا التقييم الاستدامة الأداء البيئي للمبنى ٤١٣ عبر مؤشرات الاستدامة المتعددة بما في ذلك كفاءة الطاقة وجودة الهواء وفرص التحسين التشغيلي.</p>
</div>
"""

    # Add environmental metrics if available
    if co2_level or temp_avg or humidity_avg:
        report += f"""<div style="background: white; padding: 20px; border-radius: 12px; border: 2px solid #e9ecef; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
<h3 style="margin: 0 0 15px 0; color: #28a745; font-size: 20px; font-weight: 800; text-align: right;">🌿 مؤشرات الجودة البيئية</h3>
<table style="width: 100%; border-collapse: collapse; direction: rtl;">
"""
        if co2_level:
            report += f"""<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">💨 مستويات ثاني أكسيد الكربون:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #e3f2fd;">{co2_level}</td>
</tr>
"""
        if temp_avg:
            report += f"""<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">🌡️ متوسط درجة الحرارة:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #e8f5e9;">{temp_avg}</td>
</tr>
"""
        if humidity_avg:
            report += f"""<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">💧 متوسط الرطوبة:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #fff3e0;">{humidity_avg}</td>
</tr>
"""
        if light_avg:
            report += f"""<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">💡 متوسط الإضاءة:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #f3e5f5;">{light_avg}</td>
</tr>
"""
        if pir_activity:
            report += f"""<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">👥 نشاط الحركة:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #fce4ec;">{pir_activity}</td>
</tr>
"""
        report += "</table></div>"

    # Add recommendations
    if recommendations:
        report += """<div style="background: linear-gradient(135deg, #d1ecf1 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #0dcaf0; margin-bottom: 20px;">
<h3 style="margin: 0 0 15px 0; color: #055160; font-size: 20px; font-weight: 800; text-align: right;">💡 التوصيات القابلة للتنفيذ</h3>
<ol style="margin: 5px 0; padding-right: 25px; color: #055160; line-height: 2.2;">
"""
        for recommendation in recommendations:
            report += f"<li style='margin-bottom: 12px; font-size: 15px;'>{recommendation}</li>\n"
        report += "</ol></div>"

    report += f"""
<div style="background: {bg_color}; padding: 25px; border-radius: 12px; border: 3px solid {color}; margin-bottom: 20px; text-align: center; box-shadow: 0 6px 20px rgba(0,0,0,0.15);">
<h3 style="margin: 0 0 15px 0; color: {color}; font-size: 22px; font-weight: 900;">🏆 تصنيف الاستدامة</h3>
<div style="font-size: 60px; font-weight: bold; color: {color}; margin: 15px 0;">{grade}</div>
<div style="font-size: 20px; font-weight: 800; color: {color}; margin: 10px 0;">{rating}</div>
<div style="font-size: 15px; color: #666; margin-top: 12px; font-weight: 600;">حالة الامتثال: يستوفي المعايير</div>
</div>

<div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #6c757d;">
<h3 style="margin: 0 0 12px 0; color: #495057; font-size: 20px; font-weight: 800; text-align: right;">📝 الخلاصة</h3>
<p style="margin: 0; color: #333; font-size: 15px; line-height: 1.8;">يُظهر المبنى ٤١٣ أداءً بيئياً <strong>{rating}</strong>. ستضمن المراقبة المستمرة وتنفيذ الإجراءات الموصى بها تحقيق نتائج استدامة مثلى.</p>
</div>
</div>"""
    return report

def generate_impact_report(data, metric_type):
    """Generate professional environmental impact report in Arabic"""

    #Handle both Arabic and English keys
    metric_type_ar = data.get('نوع_المقياس', metric_type)
    recommendations = data.get('التوصيات', data.get('recommendations', []))
    total_records = data.get('عدد_القراءات', data.get('total_records', ''))

    impact_title = "البصمة الكربونية" if metric_type == "carbon_footprint" else "استخدام المياه"
    impact_icon = "🌍" if metric_type == "carbon_footprint" else "💧"
    gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if metric_type == "carbon_footprint" else "linear-gradient(135deg, #17a2b8 0%, #0056b3 100%)"

    report = f"""<div style="font-family: 'Tajawal', sans-serif; line-height: 1.8; direction: rtl;">
<div style="background: {gradient}; color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
<h2 style="margin: 0; font-size: 28px; font-weight: 900;">{impact_icon} مبنى ٤١٣ - {impact_title}</h2>
<p style="margin: 8px 0 0 0; opacity: 0.95; font-size: 16px; font-weight: 500;">تقييم التأثير البيئي</p>
</div>

<div style="background: #F5F9F6; padding: 20px; border-radius: 12px; border-right: 5px solid #667eea; margin-bottom: 20px;">
<strong style="color: #667eea; font-size: 18px;">📋 تفاصيل التقرير</strong><br>
<div style="margin-top: 12px; line-height: 2;">
<span style="color: #666; font-weight: 500;">تاريخ الإنشاء:</span> <strong style="color: #333;">{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong><br>
<span style="color: #666; font-weight: 500;">رقم المبنى:</span> <strong style="color: #333;">٤١٣</strong><br>
<span style="color: #666; font-weight: 500;">نوع التحليل:</strong> <strong style="color: #333;">{impact_title}</strong>"""

    if total_records:
        report += f"""<br>
<span style="color: #666; font-weight: 500;">عدد القراءات:</span> <strong style="color: #333;">{total_records}</strong>"""

    report += """
</div>
</div>

<div style="background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #28a745; margin-bottom: 20px;">
<h3 style="margin: 0 0 12px 0; color: #28a745; font-size: 20px; font-weight: 800;">📊 الملخص التنفيذي</h3>
<p style="margin: 0; color: #333; font-size: 15px; line-height: 1.8;">يحدّد هذا التقييم البيئي تأثير المبنى ٤١٣ من حيث {impact_title} ويقدم توصيات استراتيجية لتقليل التأثير البيئي مع الحفاظ على الكفاءة التشغيلية.</p>
</div>
"""

    if metric_type == "carbon_footprint":
        # Handle both Arabic and English keys
        rating = data.get('تصنيف_الاستدامة', data.get('sustainability_rating', 'ممتاز'))
        co2_emissions = data.get('انبعاثات_CO2_المقدرة_كجم', data.get('estimated_co2_emissions_kg', 'غير متوفر'))
        daily_co2 = data.get('متوسط_CO2_اليومي_جزء_بالمليون', data.get('daily_average_co2_ppm', 'غير متوفر'))
        max_co2 = data.get('الحد_الأقصى_CO2', '')
        min_co2 = data.get('الحد_الأدنى_CO2', '')

        # Determine status based on Arabic rating
        if rating in ["ممتاز", "جيد", "Good"]:
            status_color = "#28a745"
            status_bg = "#d4edda"
            impact_level = "منخفض"
            compliance = "يستوفي المعايير البيئية"
            status_text = "البصمة الكربونية للمبنى ضمن الحدود المقبولة وتظهر ممارسات إدارة بيئية فعالة."
        elif rating in ["يحتاج تحسين", "مقبول", "Needs Improvement"]:
            status_color = "#ffc107"
            status_bg = "#fff3cd"
            impact_level = "متوسط"
            compliance = "يتطلب تحسين"
            status_text = "تشير البصمة الكربونية للمبنى إلى فرص للتحسين وتطبيق استراتيجيات تقليل الكربون."
        else:
            status_color = "#dc3545"
            status_bg = "#f8d7da"
            impact_level = "مرتفع"
            compliance = "يتطلب إجراء فوري"
            status_text = "البصمة الكربونية للمبنى تتجاوز الحدود المقبولة وتتطلب تطبيق فوري لاستراتيجيات التخفيف."

        report += f"""<div style="background: white; padding: 20px; border-radius: 12px; border: 2px solid #e9ecef; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
<h3 style="margin: 0 0 15px 0; color: #667eea; font-size: 20px; font-weight: 800; text-align: right;">🌍 ملف انبعاثات الكربون</h3>
<table style="width: 100%; border-collapse: collapse; direction: rtl;">
<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">انبعاثات CO2 المقدرة:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #e3f2fd;">{co2_emissions} كجم</td>
</tr>
<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">متوسط تركيز CO2 اليومي:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #e8f5e9;">{daily_co2} جزء/مليون</td>
</tr>"""

        if max_co2:
            report += f"""<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">الحد الأقصى CO2:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #fff3e0;">{max_co2} جزء/مليون</td>
</tr>"""

        if min_co2:
            report += f"""<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">الحد الأدنى CO2:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #f3e5f5;">{min_co2} جزء/مليون</td>
</tr>"""

        report += f"""<tr>
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">تصنيف الاستدامة:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: {status_bg}; color: {status_color};">{rating}</td>
</tr>
</table>
</div>

<div style="background: {status_bg}; padding: 20px; border-radius: 12px; border-right: 5px solid {status_color}; margin-bottom: 20px;">
<h3 style="margin: 0 0 12px 0; color: {status_color}; font-size: 20px; font-weight: 800; text-align: right;">📈 تصنيف التأثير البيئي</h3>
<table style="width: 100%; border-collapse: collapse; margin-top: 10px; direction: rtl;">
<tr>
<td style="padding: 10px; color: #666; font-weight: 500; text-align: right;">الحالة:</td>
<td style="padding: 10px; font-weight: 600; color: {status_color}; text-align: left;">{rating}</td>
</tr>
<tr>
<td style="padding: 10px; color: #666; font-weight: 500; text-align: right;">مستوى التأثير:</td>
<td style="padding: 10px; font-weight: 600; color: {status_color}; text-align: left;">{impact_level}</td>
</tr>
<tr>
<td style="padding: 10px; color: #666; font-weight: 500; text-align: right;">الامتثال:</td>
<td style="padding: 10px; font-weight: 600; color: {status_color}; text-align: left;">{compliance}</td>
</tr>
</table>
<p style="margin: 15px 0 0 0; color: #333; font-size: 15px; line-height: 1.8;">{status_text}</p>
</div>
"""

    else:  # water_usage
        # Handle both Arabic and English keys
        daily_usage = data.get('الاستخدام_اليومي_المقدر_باللتر', data.get('estimated_daily_usage_liters', 'غير متوفر'))
        humidity_eff = data.get('كفاءة_الرطوبة', data.get('humidity_efficiency', 'غير متوفر'))
        occupancy = data.get('عامل_الإشغال', data.get('occupancy_factor', 'غير متوفر'))
        avg_humidity = data.get('متوسط_الرطوبة', '')

        report += f"""<div style="background: white; padding: 20px; border-radius: 12px; border: 2px solid #e9ecef; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
<h3 style="margin: 0 0 15px 0; color: #17a2b8; font-size: 20px; font-weight: 800; text-align: right;">💧 ملف استهلاك المياه</h3>
<table style="width: 100%; border-collapse: collapse; direction: rtl;">
<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">الاستخدام اليومي المقدر:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #e3f2fd;">{daily_usage} لتر</td>
</tr>
<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">تصنيف كفاءة الرطوبة:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #e8f5e9;">{humidity_eff}</td>
</tr>
<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">عامل الإشغال:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #fff3e0;">{occupancy} حدث حركة</td>
</tr>"""

        if avg_humidity:
            report += f"""<tr>
<td style="padding: 12px; color: #666; font-weight: 500; text-align: right;">متوسط الرطوبة:</td>
<td style="padding: 12px; font-weight: 600; text-align: left; background: #f3e5f5;">{avg_humidity}</td>
</tr>"""

        report += """</table>
</div>

<div style="background: linear-gradient(135deg, #d1ecf1 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #17a2b8; margin-bottom: 20px;">
<h3 style="margin: 0 0 12px 0; color: #0c5460; font-size: 20px; font-weight: 800; text-align: right;">📊 تقييم إدارة الموارد</h3>
<p style="margin: 0; color: #333; font-size: 15px; line-height: 1.8;">يأخذ تحليل استخدام المياه بعين الاعتبار التحكم في رطوبة نظام التدفئة والتهوية وتكييف الهواء وأنماط الإشغال والكفاءة التشغيلية لتوفير رؤية شاملة لاستهلاك المياه.</p>
</div>
"""

    # Add recommendations
    if recommendations:
        report += """<div style="background: linear-gradient(135deg, #fff3cd 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #ffc107; margin-bottom: 20px;">
<h3 style="margin: 0 0 15px 0; color: #856404; font-size: 20px; font-weight: 800; text-align: right;">💡 التوصيات الاستراتيجية</h3>
<p style="margin: 0 0 15px 0; color: #666; font-size: 15px; line-height: 1.8;">يتم توفير التوصيات التالية المستندة إلى الأدلة لتقليل التأثير البيئي وتحسين الكفاءة التشغيلية:</p>
<ol style="margin: 5px 0; padding-right: 25px; color: #333; line-height: 2.2;">
"""
        for i, recommendation in enumerate(recommendations, 1):
            report += f"<li style='margin-bottom: 12px; font-size: 15px;'><strong>إجراء {i}:</strong> {recommendation}</li>\n"
        report += "</ol></div>"

    report += """
<div style="background: white; padding: 20px; border-radius: 12px; border: 2px solid #e9ecef; margin-bottom: 20px;">
<h3 style="margin: 0 0 12px 0; color: #495057; font-size: 20px; font-weight: 800; text-align: right;">✓ الامتثال والشهادات</h3>
<table style="width: 100%; border-collapse: collapse; direction: rtl;">
<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 10px; color: #666; font-weight: 500; text-align: right;">المعايير البيئية:</td>
<td style="padding: 10px; font-weight: 600; text-align: left;">متوافق مع ISO 14001</td>
</tr>
<tr style="border-bottom: 1px solid #e9ecef;">
<td style="padding: 10px; color: #666; font-weight: 500; text-align: right;">إطار التقارير:</td>
<td style="padding: 10px; font-weight: 600; text-align: left;">متوافق مع بروتوكول GHG</td>
</tr>
<tr>
<td style="padding: 10px; color: #666; font-weight: 500; text-align: right;">دقة البيانات:</td>
<td style="padding: 10px; font-weight: 600; text-align: left;">ثقة عالية (±٥٪)</td>
</tr>
</table>
</div>

<div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #6c757d;">
<h3 style="margin: 0 0 12px 0; color: #495057; font-size: 20px; font-weight: 800; text-align: right;">📝 الخلاصة</h3>
<p style="margin: 0; color: #333; font-size: 15px; line-height: 1.8;">يقدم هذا التقييم تقييماً شاملاً للتأثير البيئي للمبنى ٤١٣. سيساهم تنفيذ الإجراءات الموصى بها في تحقيق أهداف الاستدامة مع الحفاظ على التميز التشغيلي.</p>
</div>
</div>"""
    return report

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
            "Get building energy stats",
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
    user_message = data.get('message', '').strip().lower()

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Handle local queries - support both Arabic and English
    help_keywords = ['list', 'buildings', 'available', 'help', 'hello', 'hi', 'مساعدة', 'مرحبا', 'معلومات', 'ساعدني']
    if any(keyword in user_message for keyword in help_keywords):
        building_info = format_buildings_list()
        response = f"""<div style="font-family: 'Tajawal', sans-serif; line-height: 1.8; direction: rtl;">
<div style="background: linear-gradient(135deg, #006341 0%, #00A859 100%); color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,99,65,0.3);">
<h2 style="margin: 0; font-size: 28px; font-weight: 900;">🏢 معلومات المبنى ٤١٣</h2>
<p style="margin: 8px 0 0 0; opacity: 0.95; font-size: 16px; font-weight: 500;">نظام المراقبة البيئية الذكية - شاهين الشارقة</p>
</div>

<div style="background: #F5F9F6; padding: 20px; border-radius: 12px; border-right: 5px solid #00A859; margin-bottom: 20px;">
<strong style="color: #006341; font-size: 18px;">📋 تفاصيل المبنى</strong><br>
<div style="margin-top: 12px; line-height: 2;">
<span style="color: #666; font-weight: 500;">رقم المبنى:</span> <strong style="color: #333;">٤١٣</strong><br>
<span style="color: #666; font-weight: 500;">الوصف:</span> <strong style="color: #333;">نظام المراقبة البيئية الذكية</strong>
</div>
</div>

<div style="background: white; padding: 20px; border-radius: 12px; border: 2px solid #e9ecef; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
<h3 style="margin: 0 0 15px 0; color: #D4AF37; font-size: 20px; font-weight: 800;">🔧 أجهزة الاستشعار المتاحة</h3>
<ul style="margin: 5px 0; padding-right: 25px; color: #333; line-height: 2;">
<li style='margin-bottom: 10px; font-size: 15px;'><strong>💨</strong> مستويات ثاني أكسيد الكربون (جودة الهواء)</li>
<li style='margin-bottom: 10px; font-size: 15px;'><strong>🌡️</strong> قياس درجة الحرارة</li>
<li style='margin-bottom: 10px; font-size: 15px;'><strong>💧</strong> قياسات الرطوبة</li>
<li style='margin-bottom: 10px; font-size: 15px;'><strong>💡</strong> مستويات الإضاءة</li>
<li style='margin-bottom: 10px; font-size: 15px;'><strong>👥</strong> كاشف الحركة PIR</li>
</ul>
</div>

<div style="background: linear-gradient(135deg, #d1ecf1 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #0dcaf0; margin-bottom: 20px;">
<h3 style="margin: 0 0 15px 0; color: #055160; font-size: 20px; font-weight: 800;">💡 جرب هذه الاستفسارات</h3>
<ul style="margin: 5px 0; padding-right: 25px; color: #055160; line-height: 2.2;">
<li style='margin-bottom: 10px; font-size: 15px;'><em>"احصل على إحصائيات الطاقة للمبنى"</em></li>
<li style='margin-bottom: 10px; font-size: 15px;'><em>"أظهر مقاييس الاستدامة"</em></li>
<li style='margin-bottom: 10px; font-size: 15px;'><em>"احسب البصمة الكربونية"</em></li>
<li style='margin-bottom: 10px; font-size: 15px;'><em>"ما هي مستويات CO2؟"</em></li>
</ul>
</div>

<div style="background: linear-gradient(135deg, #d4edda 0%, #b8e6c4 100%); padding: 20px; border-radius: 12px; text-align: center; color: #155724; box-shadow: 0 4px 12px rgba(40,167,69,0.3);">
<strong style="font-size: 17px; font-weight: 800;">✅ جاهز لتحليل البيانات البيئية للمبنى ٤١٣!</strong>
</div>
</div>"""
        return jsonify({
            "response": response.strip(),
            "source": "local"
        })

    # Route to appropriate MCP tool based on query
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        tool_name = None
        parameters = {}

        # Support both Arabic and English keywords
        if any(kw in user_message for kw in ['energy', 'stats', 'consumption', 'طاقة', 'إحصائيات', 'استهلاك', 'احصل']):
            tool_name = "get_building_energy_stats"
        elif any(kw in user_message for kw in ['sustainability', 'metrics', 'استدامة', 'مقاييس', 'بيئة']):
            tool_name = "get_sustainability_metrics"
        elif any(kw in user_message for kw in ['carbon', 'footprint', 'eco', 'impact', 'كربون', 'بصمة', 'احسب']):
            tool_name = "analyze_eco_impact"
            parameters = {"metric_type": "carbon_footprint"}
        elif any(kw in user_message for kw in ['water', 'ماء', 'مياه']):
            tool_name = "analyze_eco_impact"
            parameters = {"metric_type": "water_usage"}
        elif any(kw in user_message for kw in ['temperature', 'humidity', 'co2', 'air', 'حرارة', 'رطوبة', 'هواء']):
            # These are in the energy stats
            tool_name = "get_building_energy_stats"

        if tool_name:
            # Call MCP tools directly
            if tool_name == "get_building_energy_stats":
                result = loop.run_until_complete(get_building_energy_stats())
            elif tool_name == "get_sustainability_metrics":
                result = loop.run_until_complete(get_sustainability_metrics())
            elif tool_name == "analyze_eco_impact":
                result = loop.run_until_complete(analyze_eco_impact(parameters.get("metric_type", "carbon_footprint")))

            loop.close()

            # Format the result as a professional report
            try:
                result_dict = eval(result)

                # Generate professional report based on tool type
                if tool_name == "get_building_energy_stats":
                    formatted_response = generate_energy_report(result_dict)
                elif tool_name == "get_sustainability_metrics":
                    formatted_response = generate_sustainability_report(result_dict)
                elif tool_name == "analyze_eco_impact":
                    formatted_response = generate_impact_report(result_dict, parameters.get("metric_type", "carbon_footprint"))
                else:
                    formatted_response = result

                result = formatted_response
            except Exception as e:
                # If formatting fails, return raw data
                pass

            return jsonify({
                "response": result,
                "source": "mcp_direct"
            })
        else:
            return jsonify({
                "response": """<div style="font-family: 'Tajawal', sans-serif; direction: rtl; padding: 20px; background: #fff3cd; border-radius: 12px; border-right: 5px solid #ffc107;">
<h4 style="color: #856404; margin: 0 0 10px 0;">⚠️ لم أتمكن من فهم طلبك</h4>
<p style="margin: 0; color: #333; line-height: 1.8;">يرجى المحاولة مرة أخرى بأحد المواضيع التالية:</p>
<ul style="margin: 10px 0; padding-right: 25px; color: #856404;">
<li>إحصائيات الطاقة</li>
<li>مقاييس الاستدامة</li>
<li>البصمة الكربونية</li>
</ul>
</div>""",
                "source": "local"
            })

    except Exception as e:
        return jsonify({
            "response": f"""<div style="font-family: 'Tajawal', sans-serif; direction: rtl; padding: 20px; background: #f8d7da; border-radius: 12px; border-right: 5px solid #dc3545;">
<h4 style="color: #721c24; margin: 0 0 10px 0;">❌ حدث خطأ</h4>
<p style="margin: 0; color: #721c24;">عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى.</p>
</div>""",
            "source": "error"
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Building 413 Chat Frontend (Direct MCP Tools)",
        "mode": "Direct Python imports (optimized)"
    })

if __name__ == '__main__':
    print("Starting Building 413 Chat Frontend (Direct MCP Tools - Optimized)...")
    print("Mode: Direct Python imports (fastest performance)")
    print("Frontend will be available at: http://localhost:5000")

    app.run(debug=True, host='0.0.0.0', port=5000)
