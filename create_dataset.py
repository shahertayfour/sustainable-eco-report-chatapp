import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate timestamps for 30 days of data (every 5 minutes)
start_date = datetime(2024, 10, 1, 0, 0, 0)
end_date = datetime(2024, 10, 30, 23, 55, 0)
timestamps = pd.date_range(start=start_date, end=end_date, freq='5T')

# Initialize lists to store data
data = []

for ts in timestamps:
    hour = ts.hour
    day_of_week = ts.dayofweek  # Monday=0, Sunday=6

    # CO2 levels (ppm) - higher during working hours, lower at night
    # Sharjah business hours typically 8 AM - 6 PM
    if 8 <= hour <= 18 and day_of_week < 5:  # Working hours on weekdays
        co2_base = 520
        co2_variation = np.random.normal(0, 30)
        # Peak during lunch time
        if 12 <= hour <= 14:
            co2_base += 40
    elif 6 <= hour <= 22:  # Evening/early morning
        co2_base = 460
        co2_variation = np.random.normal(0, 20)
    else:  # Night time
        co2_base = 420
        co2_variation = np.random.normal(0, 15)

    co2 = max(400, min(600, co2_base + co2_variation))

    # Temperature (°C) - Sharjah climate patterns
    # Hotter during day, cooler at night
    if 6 <= hour <= 18:  # Daytime
        temp_base = 25.5
        temp_variation = np.random.normal(0, 0.5)
        # Peak temperature around 2-4 PM
        if 14 <= hour <= 16:
            temp_base += 1.2
    else:  # Night time
        temp_base = 23.5
        temp_variation = np.random.normal(0, 0.3)

    temperature = round(temp_base + temp_variation, 2)

    # Humidity (%) - Lower during day due to AC, higher at night
    if 8 <= hour <= 18:
        humidity_base = 42.5
        humidity_variation = np.random.normal(0, 1.5)
    else:
        humidity_base = 45.0
        humidity_variation = np.random.normal(0, 1.0)

    humidity = round(max(35, min(55, humidity_base + humidity_variation)), 2)

    # Light levels (lux) - based on occupancy and time of day
    if 8 <= hour <= 18 and day_of_week < 5:  # Working hours
        light_base = 180
        light_variation = np.random.normal(0, 30)
    elif 6 <= hour <= 22:  # Some lighting
        light_base = 80
        light_variation = np.random.normal(0, 20)
    else:  # Night time - minimal lighting
        light_base = 5
        light_variation = np.random.normal(0, 3)

    light = round(max(0, light_base + light_variation), 1)

    # PIR Motion Detection (0 or 1)
    # Higher probability during working hours
    if 8 <= hour <= 18 and day_of_week < 5:  # Working hours
        pir = 1 if np.random.random() > 0.3 else 0
    elif 18 <= hour <= 22:  # Evening
        pir = 1 if np.random.random() > 0.7 else 0
    else:  # Night/weekend
        pir = 1 if np.random.random() > 0.9 else 0

    # Add some seasonal variations
    day_of_month = ts.day
    seasonal_factor = np.sin(day_of_month / 30 * np.pi) * 0.5

    # Append data
    data.append({
        'datetime': ts.strftime('%Y-%m-%d %H:%M:%S'),
        'co2': round(co2, 1),
        'humidity': round(humidity + seasonal_factor, 2),
        'temperature': round(temperature + seasonal_factor * 0.5, 2),
        'light': round(light, 1),
        'pir': float(pir),
        'building_id': 413
    })

# Create DataFrame
df = pd.DataFrame(data)

# Add some realistic variations and anomalies
# 1. Add occasional high CO2 spikes (poor ventilation events)
spike_indices = np.random.choice(len(df), size=50, replace=False)
df.loc[spike_indices, 'co2'] = df.loc[spike_indices, 'co2'] * 1.15

# 2. Add occasional temperature variations (AC adjustments)
temp_indices = np.random.choice(len(df), size=100, replace=False)
df.loc[temp_indices, 'temperature'] = df.loc[temp_indices, 'temperature'] + np.random.normal(0, 1, size=100)

# 3. Add weekend patterns - lower activity
weekend_mask = pd.to_datetime(df['datetime']).dt.dayofweek >= 5
df.loc[weekend_mask, 'co2'] = df.loc[weekend_mask, 'co2'] * 0.85
df.loc[weekend_mask, 'light'] = df.loc[weekend_mask, 'light'] * 0.3
df.loc[weekend_mask, 'pir'] = 0

# Round all numeric columns
df['co2'] = df['co2'].round(1)
df['temperature'] = df['temperature'].round(2)
df['humidity'] = df['humidity'].round(2)
df['light'] = df['light'].round(1)

# Ensure values are within realistic ranges
df['co2'] = df['co2'].clip(400, 650)
df['temperature'] = df['temperature'].clip(22, 28)
df['humidity'] = df['humidity'].clip(35, 55)
df['light'] = df['light'].clip(0, 250)

# Save to CSV
output_path = 'dataset/building_413_data.csv'
df.to_csv(output_path, index=False)

# Print statistics
print("Dataset Created Successfully!")
print(f"\nTotal Records: {len(df)}")
print(f"\nDate Range: {df['datetime'].min()} to {df['datetime'].max()}")
print(f"\nData Statistics:")
print(df[['co2', 'humidity', 'temperature', 'light', 'pir']].describe())
print(f"\nDataset saved to: {output_path}")
print(f"\nSample Data:")
print(df.head(10))
