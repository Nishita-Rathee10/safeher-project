import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load our movement data
df = pd.read_csv("movement_data.csv")
features = df[["latitude", "longitude", "speed"]]

# Train the model (same as before)
model = IsolationForest(contamination=0.025, random_state=42)
model.fit(features)

# Save the trained model to a file
joblib.dump(model, "anomaly_model.pkl")

print("Model saved successfully as anomaly_model.pkl")