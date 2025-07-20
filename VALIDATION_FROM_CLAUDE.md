# Dataset Relevancy Analysis Report
## Building 413 Sustainability Report vs. Attached Dataset

### Executive Summary
The sustainability report is relevant to the attached dataset, but with significant limitations. While the dataset confirms this is Building 413 and demonstrates environmental monitoring capabilities, it represents only a small historical snapshot (August 2013) that cannot validate the comprehensive metrics and future goals outlined in the sustainability report.

## Key Findings

### ✓ Confirmed Relevance

1. **Correct Building**
   - The dataset contains sensor data exclusively from Building 413, matching the subject of the sustainability report.

2. **Environmental Monitoring**
   - The dataset includes the type of sensor data (CO2, temperature, humidity, light, motion detection) that would be used for building sustainability monitoring.

3. **Occupancy Patterns Align**
   - The data shows zero motion detection during late night hours (11pm-4am), which perfectly aligns with the report's stated peak occupancy of 7am-6pm on weekdays.

4. **Energy Efficiency Indicators**
   - Low light levels (average 80.6 lux) during nighttime hours
   - Stable temperature maintenance (~24.8°C)
   - Low CO2 levels (~492 ppm) consistent with an unoccupied building

### ⚠️ Important Limitations

1. **Time Gap**
   - The dataset is from August 2013, while the sustainability report discusses goals for 2023-2030 - a 10+ year gap.

2. **Limited Duration**
   - The data covers only 1-2 days, making it impossible to verify the annual metrics mentioned in the report (1,200 MWh electricity consumption, 100,000 gallons water usage, etc.).

3. **Partial Coverage**
   - The dataset only contains nighttime/off-hours data and doesn't capture the peak occupancy periods that would be crucial for validating energy consumption patterns.

4. **Missing Metrics**
   - The sensor data cannot verify many key sustainability metrics mentioned in the report, such as:
     - Actual energy consumption in kW/MWh
     - Water usage
     - Waste generation
     - Tenant-specific energy use

## Dataset Analysis Details

### Dataset Overview
- **Building ID**: 413
- **Total records**: 10,000
- **Date range**: August 23-24, 2013 (Friday night to Saturday morning)
- **Time period**: 11:05 PM to 4:59 AM

### Environmental Sensor Data
- **CO2 levels**: 438-568 ppm (average: 492.1 ppm)
- **Temperature**: 23.9-25.3°C (average: 24.8°C)
- **Light levels**: 0-238 lux (average: 80.6 lux)
- **Humidity**: 29.1-51.9% (when recorded)

### Occupancy Analysis
- **Motion detected**: 0 times out of 2,129 readings (0.0%)
- **Time period**: Late night (11pm-4am) - building expected to be unoccupied
- **PIR sensor coverage**: Approximately 21% of total readings included PIR data

### Data Quality
- **CO2**: 91.7% complete (831 null values)
- **Temperature**: 85.4% complete (1,463 null values)
- **Humidity**: 85.4% complete (1,463 null values)
- **Light**: 85.4% complete (1,463 null values)
- **PIR**: 78.7% complete (2,129 null values)

## Conclusion

While this dataset is indeed from Building 413 and demonstrates the type of environmental monitoring that supports sustainability reporting, it represents only a tiny snapshot of the building's operations from 2013. The report appears to be based on much more comprehensive and recent data than what's provided in this CSV file.

The dataset could be considered a historical example of the building's monitoring capabilities but cannot validate the specific sustainability metrics and goals outlined in the report. To properly verify the sustainability report's claims, one would need:

1. Current data from 2023-2025
2. Full 24-hour coverage including peak occupancy periods
3. Direct energy consumption measurements
4. Water usage data
5. Waste management metrics
6. At least 12 months of continuous data to verify annual figures

## Recommendation

The sustainability report and dataset are related but not directly comparable due to the temporal gap and limited scope of the sensor data. The dataset serves as evidence that Building 413 has environmental monitoring infrastructure in place, which is a prerequisite for the comprehensive sustainability tracking described in the report.