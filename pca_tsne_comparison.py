import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Load our movement data (with predictions from Isolation Forest)
df = pd.read_csv("movement_data_with_predictions.csv")

# Use the same features as before
features = df[["latitude", "longitude", "speed"]]

# ===== PCA =====
# n_components=2 means we want to compress everything down to 2 dimensions
pca = PCA(n_components=2)
pca_result = pca.fit_transform(features)

# Add the PCA results as new columns
df["pca_x"] = pca_result[:, 0]
df["pca_y"] = pca_result[:, 1]

# ===== t-SNE =====
# perplexity controls how t-SNE balances local vs global structure (30 is a common default)
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
tsne_result = tsne.fit_transform(features)

df["tsne_x"] = tsne_result[:, 0]
df["tsne_y"] = tsne_result[:, 1]

# ===== Plot both side-by-side =====
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# PCA plot (left side)
normal_pca = df[df["is_anomaly"] == 0]
anomaly_pca = df[df["is_anomaly"] == 1]
axes[0].scatter(normal_pca["pca_x"], normal_pca["pca_y"], c="blue", label="Normal", alpha=0.5, s=20)
axes[0].scatter(anomaly_pca["pca_x"], anomaly_pca["pca_y"], c="red", label="Anomaly", alpha=0.8, s=50)
axes[0].set_title("PCA - 2D Projection")
axes[0].legend()

# t-SNE plot (right side)
normal_tsne = df[df["is_anomaly"] == 0]
anomaly_tsne = df[df["is_anomaly"] == 1]
axes[1].scatter(normal_tsne["tsne_x"], normal_tsne["tsne_y"], c="blue", label="Normal", alpha=0.5, s=20)
axes[1].scatter(anomaly_tsne["tsne_x"], anomaly_tsne["tsne_y"], c="red", label="Anomaly", alpha=0.8, s=50)
axes[1].set_title("t-SNE - 2D Projection")
axes[1].legend()

plt.tight_layout()
plt.savefig("pca_vs_tsne.png")
plt.show()

print("Comparison graph saved as pca_vs_tsne.png")