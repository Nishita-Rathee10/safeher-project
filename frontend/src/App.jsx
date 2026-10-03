import { useState, useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "./App.css";

function App() {
  const [zones, setZones] = useState([]);
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [speed, setSpeed] = useState("");
  const [result, setResult] = useState(null);
  const [pcaTsneData, setPcaTsneData] = useState([]);
  const [gracePeriodActive, setGracePeriodActive] = useState(false);
  const [countdown, setCountdown] = useState(10);

  useEffect(() => {
    fetch("https://safeher-project.onrender.com/unsafe-zones")
      .then((response) => response.json())
      .then((data) => {
        setZones(data.unsafe_zones);
      })
      .catch((error) => {
        console.error("Error fetching zones:", error);
      });

    fetch("https://safeher-project.onrender.com/pca-tsne-data")
      .then((response) => response.json())
      .then((data) => {
        setPcaTsneData(data.points);
      })
      .catch((error) => {
        console.error("Error fetching PCA/t-SNE data:", error);
      });
  }, []);

  useEffect(() => {
    if (!gracePeriodActive) return;

    if (countdown === 0) {
      setGracePeriodActive(false);
      setResult({ is_anomaly: true, message: "No response received. Alert sent to emergency contacts!" });
      return;
    }

    const timer = setTimeout(() => {
      setCountdown(countdown - 1);
    }, 1000);

    return () => clearTimeout(timer);
  }, [gracePeriodActive, countdown]);

  const mapCenter = [28.63, 77.22];

  const handleCheck = () => {
    fetch("https://safeher-project.onrender.com/check-anomaly", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        speed: parseFloat(speed),
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data);
        if (data.is_anomaly) {
          setGracePeriodActive(true);
          setCountdown(10);
        }
      })
      .catch((error) => {
        console.error("Error checking anomaly:", error);
      });
  };

  const handleImOkay = () => {
    setGracePeriodActive(false);
    setResult({ is_anomaly: false, message: "Great, glad you're safe! Alert cancelled." });
  };

  const renderScatterPlot = (data, xKey, yKey) => {
    if (data.length === 0) return null;

    const xValues = data.map((d) => d[xKey]);
    const yValues = data.map((d) => d[yKey]);
    const xMin = Math.min(...xValues);
    const xMax = Math.max(...xValues);
    const yMin = Math.min(...yValues);
    const yMax = Math.max(...yValues);

    const scaleX = (x) => 20 + ((x - xMin) / (xMax - xMin)) * 260;
    const scaleY = (y) => 280 - ((y - yMin) / (yMax - yMin)) * 260;

    return (
      <svg width="300" height="300" style={{ background: "#1a1d29", borderRadius: "8px" }}>
        {data.map((point, index) => (
          <circle
            key={index}
            cx={scaleX(point[xKey])}
            cy={scaleY(point[yKey])}
            r={point.is_anomaly ? 5 : 3}
            fill={point.is_anomaly ? "#ff4d6d" : "#5b8def"}
            opacity={point.is_anomaly ? 1 : 0.6}
          />
        ))}
      </svg>
    );
  };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">SafeHer</h1>
      <p className="dashboard-subtitle">AI-Powered Personal Safety Dashboard</p>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🗺️</div>
          <div className="stat-value">{zones.length}</div>
          <div className="stat-label">Unsafe Zones Mapped</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📍</div>
          <div className="stat-value">
            {zones.reduce((sum, zone) => sum + zone.incident_count, 0)}
          </div>
          <div className="stat-label">Incidents Analyzed</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🧠</div>
          <div className="stat-value">3</div>
          <div className="stat-label">ML Techniques Used</div>
        </div>
      </div>

      <h2 className="section-heading">Unsafe Zones Map</h2>
      <div className="map-wrapper">
        <MapContainer
          center={mapCenter}
          zoom={12}
          style={{ height: "500px", width: "100%" }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; OpenStreetMap contributors'
          />
          {zones.map((zone) => (
            <CircleMarker
              key={zone.zone_id}
              center={[zone.center_latitude, zone.center_longitude]}
              radius={15}
              pathOptions={{ color: "#ff4d6d", fillColor: "#ff4d6d", fillOpacity: 0.5 }}
            >
              <Popup>
                <strong>Zone {zone.zone_id}</strong>
                <br />
                Incidents: {zone.incident_count}
                <br />
                Peak risk hours: {zone.peak_risk_hours.join(", ")}
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

      <h2 className="section-heading">Check Movement Anomaly</h2>
      <div className="check-form">
        <input
          type="number"
          placeholder="Latitude"
          value={latitude}
          onChange={(e) => setLatitude(e.target.value)}
        />
        <input
          type="number"
          placeholder="Longitude"
          value={longitude}
          onChange={(e) => setLongitude(e.target.value)}
        />
        <input
          type="number"
          placeholder="Speed"
          value={speed}
          onChange={(e) => setSpeed(e.target.value)}
        />
        <button className="check-button" onClick={handleCheck}>
          Check
        </button>
      </div>

      {gracePeriodActive && (
        <div className="result-box result-anomaly">
          <strong>⚠️ Unusual movement detected!</strong>
          <br />
          Are you okay? Alerting your emergency contacts in {countdown} seconds...
          <br />
          <button className="check-button" style={{ marginTop: "10px" }} onClick={handleImOkay}>
            I'm Okay
          </button>
        </div>
      )}

      {!gracePeriodActive && result && (
        <div className={`result-box ${result.is_anomaly ? "result-anomaly" : "result-normal"}`}>
          <strong>{result.is_anomaly ? "⚠️ Alert Sent!" : "✅ All Good"}</strong>
          <br />
          {result.message}
        </div>
      )}

      <h2 className="section-heading" style={{ marginTop: "30px" }}>PCA vs t-SNE Comparison</h2>
      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        <div>
          <p style={{ textAlign: "center", color: "#9ca3af", marginBottom: "8px" }}>PCA</p>
          {renderScatterPlot(pcaTsneData, "pca_x", "pca_y")}
        </div>
        <div>
          <p style={{ textAlign: "center", color: "#9ca3af", marginBottom: "8px" }}>t-SNE</p>
          {renderScatterPlot(pcaTsneData, "tsne_x", "tsne_y")}
        </div>
      </div>
    </div>
  );
}

export default App;