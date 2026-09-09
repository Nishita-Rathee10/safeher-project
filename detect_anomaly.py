import pandas as pd
from sklearn.ensemble import IsolationForest

# Load the data we generated earlier
df = pd.read_csv("movement_data.csv")

# We only give the model these 3 features - latitude, longitude, speed
# (We do NOT give the is_anomaly column - that's the whole point of unsupervised learning)
features = df[["latitude", "longitude", "speed"]]

# Create the Isolation Forest model
# contamination=0.05 means we expect roughly 5% of the data to be anomalies
model = IsolationForest(contamination=0.025, random_state=42)

# Train the model on our data (this is the "learning" step)
model.fit(features)

# Get predictions - for each row, the model decides normal or anomaly
# Output: -1 means anomaly, 1 means normal
df["prediction"] = model.predict(features)

# Convert -1/1 into 1/0 format to match our is_anomaly column
df["predicted_anomaly"] = df["prediction"].apply(lambda x: 1 if x == -1 else 0)

# Compare model's predictions against our actual is_anomaly labels
print("Total anomalies predicted by model:", df["predicted_anomaly"].sum())
print("Actual number of anomalies:", df["is_anomaly"].sum())

# Simple comparison - how many correct, how many wrong
correct_anomaly_catches = df[(df["is_anomaly"] == 1) & (df["predicted_anomaly"] == 1)]
missed_anomalies = df[(df["is_anomaly"] == 1) & (df["predicted_anomaly"] == 0)]
false_alarms = df[(df["is_anomaly"] == 0) & (df["predicted_anomaly"] == 1)]

print(f"\nCorrectly caught anomalies: {len(correct_anomaly_catches)}")
print(f"Missed anomalies: {len(missed_anomalies)}")
print(f"False alarms (normal points wrongly flagged): {len(false_alarms)}")

# Save results to a new CSV so we can visualize later
df.to_csv("movement_data_with_predictions.csv", index=False)
print("\nResults saved to: movement_data_with_predictions.csv")