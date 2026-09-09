import pandas as pd
import matplotlib.pyplot as plt

# Humara generated data load karo
df = pd.read_csv("movement_data.csv")

# Ek plot banate hain jisme saari locations dikhengi
plt.figure(figsize=(10, 8))

# Normal points (is_anomaly = 0) ko blue color mein dikhao
normal_data = df[df["is_anomaly"] == 0]
plt.scatter(normal_data["longitude"], normal_data["latitude"], 
            c="blue", label="Normal", alpha=0.5, s=20)

# Anomaly points (is_anomaly = 1) ko red color mein dikhao
anomaly_data = df[df["is_anomaly"] == 1]
plt.scatter(anomaly_data["longitude"], anomaly_data["latitude"], 
            c="red", label="Anomaly", alpha=0.8, s=50)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Priya's Movement Pattern - Normal vs Anomaly")
plt.legend()
plt.savefig("movement_plot.png")  # graph ko image file mein save karega
plt.show()  # graph ko screen pe bhi dikhayega

print("Graph ban gaya! Check karo movement_plot.png file")