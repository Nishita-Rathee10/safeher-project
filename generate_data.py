import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Priya ka "home" aur "college" location fix kar rahe hain (imaginary coordinates)
HOME_LAT, HOME_LON = 28.6139, 77.2090      # Delhi jaisa koi area
COLLEGE_LAT, COLLEGE_LON = 28.6304, 77.2177 # thoda door, college jaisa area

def generate_normal_day(date, user_id):
    """Ek NORMAL din ka data generate karta hai"""
    records = []
    
    # Subah ghar se nikalti hai, time thoda vary karta hai (7:45 - 8:15 AM)
    start_hour = 7 + random.uniform(0.75, 1.25)
    
    # Ghar se college tak movement simulate karo (10 points, gradually location change)
    for i in range(10):
        fraction = i / 9  # 0 se 1 tak
        lat = HOME_LAT + (COLLEGE_LAT - HOME_LAT) * fraction
        lon = HOME_LON + (COLLEGE_LON - HOME_LON) * fraction
        timestamp = date.replace(hour=int(start_hour), minute=int((start_hour % 1) * 60)) + timedelta(minutes=i*3)
        speed = random.uniform(15, 25)  # normal travel speed (km/h jaisa)
        
        records.append({
            "user_id": user_id,
            "timestamp": timestamp,
            "latitude": lat,
            "longitude": lon,
            "speed": speed,
            "is_anomaly": 0   # normal hai, isliye 0
        })
    
    # College mein pura din rehti hai (ek fixed location pe, speed 0 - stationary)
    for i in range(5):
        timestamp = date.replace(hour=9, minute=0) + timedelta(hours=i)
        records.append({
            "user_id": user_id,
            "timestamp": timestamp,
            "latitude": COLLEGE_LAT,
            "longitude": COLLEGE_LON,
            "speed": 0,
            "is_anomaly": 0
        })
    
    # Shaam ko wapas ghar (reverse movement)
    for i in range(10):
        fraction = i / 9
        lat = COLLEGE_LAT + (HOME_LAT - COLLEGE_LAT) * fraction
        lon = COLLEGE_LON + (HOME_LON - COLLEGE_LON) * fraction
        timestamp = date.replace(hour=17, minute=0) + timedelta(minutes=i*3)
        speed = random.uniform(15, 25)
        
        records.append({
            "user_id": user_id,
            "timestamp": timestamp,
            "latitude": lat,
            "longitude": lon,
            "speed": speed,
            "is_anomaly": 0
        })
    
    return records


def generate_anomaly_day(date, user_id):
    """Ek ANOMALY din generate karta hai - kuch ajeeb pattern"""
    records = []
    
    # Normal subah ki tarah ghar se nikalti hai
    for i in range(10):
        fraction = i / 9
        lat = HOME_LAT + (COLLEGE_LAT - HOME_LAT) * fraction
        lon = HOME_LON + (COLLEGE_LON - HOME_LON) * fraction
        timestamp = date.replace(hour=8, minute=0) + timedelta(minutes=i*3)
        speed = random.uniform(15, 25)
        records.append({
            "user_id": user_id, "timestamp": timestamp,
            "latitude": lat, "longitude": lon, "speed": speed, "is_anomaly": 0
        })
    
    # ANOMALY: Raat ko ek bilkul ANJAAN location pe, bahut der tak ruki hui (speed 0)
    unknown_lat = HOME_LAT + random.uniform(0.05, 0.1)  # college se bhi door, alag direction
    unknown_lon = HOME_LON + random.uniform(0.05, 0.1)
    
    for i in range(6):  # 6 baar record, matlab lambe time tak ek hi jagah
        timestamp = date.replace(hour=23, minute=0) + timedelta(minutes=i*10)
        records.append({
            "user_id": user_id,
            "timestamp": timestamp,
            "latitude": unknown_lat,
            "longitude": unknown_lon,
            "speed": 0,          # bilkul stationary - suspicious
            "is_anomaly": 1      # ye anomaly hai, isliye 1
        })
    
    return records


# ===== Main data generation =====
all_records = []
start_date = datetime(2026, 1, 1)

for day in range(30):  # 30 din ka data banayenge
    current_date = start_date + timedelta(days=day)
    
    # 27 din normal, 3 din anomaly (random pick)
    if day in [10, 19, 25]:  # ye specific din anomaly wale honge
        all_records.extend(generate_anomaly_day(current_date, user_id="priya_001"))
    else:
        all_records.extend(generate_normal_day(current_date, user_id="priya_001"))

# DataFrame banao (pandas ka table jaisa structure) aur CSV file mein save karo
df = pd.DataFrame(all_records)
df.to_csv("movement_data.csv", index=False)

print(f"Total {len(df)} records generate hue")
print(f"Anomaly records: {df['is_anomaly'].sum()}")
print("File saved as movement_data.csv")