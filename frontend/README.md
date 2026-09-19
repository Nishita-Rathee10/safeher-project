# 🆘 SafeHer — AI-Powered Personal Safety Dashboard

SafeHer is a prototype safety application that uses **unsupervised machine learning** to detect abnormal personal movement patterns and map city-wide unsafe zones — enabling faster, automatic emergency response instead of relying on manual SOS alerts.

🔗 **Live Demo:** [safeher-project-seven.vercel.app](https://safeher-project-seven.vercel.app)  
🔗 **Backend API:** [safeher-project.onrender.com](https://safeher-project.onrender.com)

---

## 📌 Problem Statement

Most personal safety apps rely on the victim manually pressing an SOS button — but in real emergencies, this is often not possible. SafeHer flips this model: it learns a person's normal movement pattern and automatically detects deviations that may indicate distress, without requiring any manual action.

## ✨ Features

- **Personal Anomaly Detection** — Uses Isolation Forest and Local Outlier Factor (LOF) to learn a user's normal movement baseline and flag unusual deviations (unfamiliar location, unusual stop duration, off-hours activity).
- **City Unsafe Zone Mapping** — Uses DBSCAN clustering on incident report data to identify genuine high-risk zones, distinguishing them from random one-off complaints (noise).
- **Time-of-Day Risk Analysis** — Identifies peak risk hours for each unsafe zone.
- **Interactive Map Dashboard** — Built with React and Leaflet, showing live unsafe zones on an OpenStreetMap-based map.
- **Real-Time Anomaly Check** — A live form that checks any location/speed input against the trained model and returns an instant result.
- **PCA vs t-SNE Visualization** — Compares linear and non-linear dimensionality reduction techniques to visualize how anomalies separate from normal patterns.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Machine Learning | Python, scikit-learn (Isolation Forest, LOF, DBSCAN, PCA, t-SNE) |
| Backend | FastAPI |
| Frontend | React (Vite), Leaflet |
| Deployment | Render (backend), Vercel (frontend) |

## 📊 Model Performance

On synthetic validation data:
- **Recall:** 100% (all injected anomalies correctly detected)
- **Precision:** ~94.7% (minimal false alarms)

## 📁 Project Structure
safepath/
├── generate_data.py # Synthetic movement data generator
├── generate_incidents.py # Synthetic incident report generator
├── detect_anomaly.py # Isolation Forest model
├── detect_anomaly_lof.py # LOF model (comparison)
├── cluster_zones.py # DBSCAN clustering
├── zone_risk_analysis.py # Time-of-day risk analysis
├── pca_tsne_comparison.py # PCA vs t-SNE visualization
├── save_model.py # Saves trained model for backend use
├── main.py # FastAPI backend
└── frontend/ # React dashboard

## 🚀 Running Locally

**Backend:**
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## ⚠️ Note on Data

This project uses **synthetic (simulated) data** for both movement patterns and incident reports, as real personal safety data is not ethically available for public use. The system is a working prototype demonstrating the underlying methodology, validated against known injected anomalies.

