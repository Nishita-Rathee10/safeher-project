import pandas as pd
from sklearn.neighbors import LocalOutlierFactor

# Load the same data we generated earlier
df = pd.read_csv("movement_data.csv")

# Same 3 features as before - latitude, longitude, speed
features = df[["latitude", "longitude", "speed"]]

# Create the LOF model
# n_neighbors = how many nearby points to compare each point against (its "local group")
# contamination = expected percentage of anomalies, same as before
lof_model = LocalOutlierFactor(n_neighbors=20, contamination=0.025)

# LOF works a bit differently - fit_predict does both training and prediction in one step
# Output: -1 means anomaly, 1 means normal (same as Isolation Forest)
df["lof_prediction"] = lof_model.fit_predict(features)

# Convert -1/1 into 1/0 format
df["lof_predicted_anomaly"] = df["lof_prediction"].apply(lambda x: 1 if x == -1 else 0)

# Compare LOF's predictions against actual is_anomaly labels
print("Total anomalies predicted by LOF:", df["lof_predicted_anomaly"].sum())
print("Actual number of anomalies:", df["is_anomaly"].sum())

correct_catches = df[(df["is_anomaly"] == 1) & (df["lof_predicted_anomaly"] == 1)]
missed = df[(df["is_anomaly"] == 1) & (df["lof_predicted_anomaly"] == 0)]
false_alarms = df[(df["is_anomaly"] == 0) & (df["lof_predicted_anomaly"] == 1)]

print(f"\nCorrectly caught anomalies (LOF): {len(correct_catches)}")
print(f"Missed anomalies (LOF): {len(missed)}")
print(f"False alarms (LOF): {len(false_alarms)}")

# Save results
df.to_csv("movement_data_with_lof_predictions.csv", index=False)
print("\nResults saved to: movement_data_with_lof_predictions.csv")