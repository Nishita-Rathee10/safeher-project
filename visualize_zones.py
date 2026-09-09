import pandas as pd
import matplotlib.pyplot as plt

# Load the clustered incident data
df = pd.read_csv("incident_data_with_clusters.csv")

plt.figure(figsize=(10, 8))

# Get all unique cluster labels (0, 1, 2, -1)
unique_clusters = df["cluster"].unique()

# We'll assign a different color to each cluster
colors = ["red", "orange", "purple", "gray"]  # gray will be used for noise (-1)

for cluster_label in sorted(unique_clusters):
    cluster_points = df[df["cluster"] == cluster_label]
    
    if cluster_label == -1:
        # Noise points - plot them as gray, smaller, labeled "Noise"
        plt.scatter(cluster_points["longitude"], cluster_points["latitude"],
                    c="gray", label="Noise (no pattern)", alpha=0.5, s=30, marker="x")
    else:
        plt.scatter(cluster_points["longitude"], cluster_points["latitude"],
                    label=f"Unsafe Zone {cluster_label}", alpha=0.7, s=60)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("City Unsafe Zones - DBSCAN Clustering Result")
plt.legend()
plt.savefig("zones_plot.png")
plt.show()

print("Graph saved as zones_plot.png")