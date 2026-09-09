import pandas as pd
import numpy as np
import random

# We'll create 3 "real" unsafe zones in the city, plus some random scattered noise
# Each zone is a center point (lat, lon) around which incidents will cluster

np.random.seed(42)
random.seed(42)

records = []

# ===== Zone 1: A busy market area with poor lighting - many incidents =====
zone1_center = (28.640, 77.220)
for i in range(15):
    lat = zone1_center[0] + np.random.normal(0, 0.002)
    lon = zone1_center[1] + np.random.normal(0, 0.002)
    hour = random.choice([20, 21, 22, 23])  # mostly evening/night incidents
    records.append({"latitude": lat, "longitude": lon, "hour": hour, "incident_type": "harassment_report"})

# ===== Zone 2: An isolated underpass area - fewer but concentrated incidents =====
zone2_center = (28.610, 77.235)
for i in range(10):
    lat = zone2_center[0] + np.random.normal(0, 0.0015)
    lon = zone2_center[1] + np.random.normal(0, 0.0015)
    hour = random.choice([22, 23, 0, 1])  # late night
    records.append({"latitude": lat, "longitude": lon, "hour": hour, "incident_type": "poor_lighting_complaint"})

# ===== Zone 3: A construction area - moderate incidents =====
zone3_center = (28.655, 77.200)
for i in range(12):
    lat = zone3_center[0] + np.random.normal(0, 0.002)
    lon = zone3_center[1] + np.random.normal(0, 0.002)
    hour = random.choice([19, 20, 21])
    records.append({"latitude": lat, "longitude": lon, "hour": hour, "incident_type": "harassment_report"})

# ===== Random scattered noise - one-off complaints spread across the city =====
# These should NOT form a cluster, they're just isolated single reports
for i in range(8):
    lat = 28.6 + random.uniform(0, 0.08)
    lon = 77.18 + random.uniform(0, 0.08)
    hour = random.choice(range(24))
    records.append({"latitude": lat, "longitude": lon, "hour": hour, "incident_type": "misc_complaint"})

df = pd.DataFrame(records)
df.to_csv("incident_data.csv", index=False)

print(f"Total incidents generated: {len(df)}")
print("File saved as incident_data.csv")