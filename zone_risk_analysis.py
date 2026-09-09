import pandas as pd

# Load the clustered data
df = pd.read_csv("incident_data_with_clusters.csv")

# Remove noise points - we only care about real zones (cluster 0, 1, 2...)
zones_only = df[df["cluster"] != -1]

# For each zone, find out which hours have the most incidents
print("=== Risk Analysis by Zone ===\n")

for cluster_id in sorted(zones_only["cluster"].unique()):
    zone_data = zones_only[zones_only["cluster"] == cluster_id]
    
    # Find the most common hours for incidents in this zone
    common_hours = zone_data["hour"].value_counts().sort_index()
    
    # Determine risk level based on hour range
    peak_hours = zone_data["hour"].mode().tolist()  # most frequent hour(s)
    
    print(f"Unsafe Zone {cluster_id}:")
    print(f"  Total incidents: {len(zone_data)}")
    print(f"  Peak risk hours: {sorted(peak_hours)}")
    print(f"  Incident type(s): {zone_data['incident_type'].unique().tolist()}")
    print()