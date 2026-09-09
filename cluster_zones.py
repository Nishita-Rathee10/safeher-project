import pandas as pd
from sklearn.cluster import DBSCAN

# Load the incident data we just generated
df = pd.read_csv("incident_data.csv")

# We only give DBSCAN the location - latitude and longitude
# (hour and incident_type are not used for clustering right now, just location-based grouping)
features = df[["latitude", "longitude"]]

# eps = how close points need to be to count as "nearby" (in degrees, roughly ~0.005 = ~500m)
# min_samples = minimum number of points needed to form a cluster
dbscan_model = DBSCAN(eps=0.005, min_samples=5)

# fit_predict does the clustering and returns a cluster label for each point
# Label -1 means "noise" (not part of any cluster)
# Labels 0, 1, 2... mean the point belongs to that cluster number
df["cluster"] = dbscan_model.fit_predict(features)

# Let's see what clusters were found
print("Cluster labels found:", df["cluster"].unique())
print("\nHow many points in each cluster:")
print(df["cluster"].value_counts())

# Count how many points were marked as noise
noise_count = (df["cluster"] == -1).sum()
print(f"\nPoints marked as noise (not in any unsafe zone cluster): {noise_count}")

# Save the result
df.to_csv("incident_data_with_clusters.csv", index=False)
print("\nResults saved to: incident_data_with_clusters.csv")