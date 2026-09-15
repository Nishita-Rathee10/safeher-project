from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from pydantic import BaseModel

# Create the FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# A simple "home" endpoint just to test that the server works
@app.get("/")
def home():
    return {"message": "SafeHer backend is running"}

# Endpoint that returns the list of unsafe zones with their risk info
@app.get("/unsafe-zones")
def get_unsafe_zones():
    # Load our clustered incident data
    df = pd.read_csv("incident_data_with_clusters.csv")
    
    # Remove noise points, we only want real zones
    zones_only = df[df["cluster"] != -1]
    
    zone_list = []
    for cluster_id in sorted(zones_only["cluster"].unique()):
        zone_data = zones_only[zones_only["cluster"] == cluster_id]
        
        zone_info = {
            "zone_id": int(cluster_id),
            "incident_count": len(zone_data),
            "peak_risk_hours": sorted(zone_data["hour"].mode().tolist()),
            "center_latitude": float(zone_data["latitude"].mean()),
            "center_longitude": float(zone_data["longitude"].mean()),
        }
        zone_list.append(zone_info)
    
    return {"unsafe_zones": zone_list}


#new code
# Load the saved model once, when the server starts
saved_model = joblib.load("anomaly_model.pkl")

# We need a way to receive data from the frontend - this defines the shape of that data
from pydantic import BaseModel

class MovementPoint(BaseModel):
    latitude: float
    longitude: float
    speed: float

# POST endpoint - frontend sends a new movement point, we check if it's an anomaly
@app.post("/check-anomaly")
def check_anomaly(point: MovementPoint):
    input_data = [[point.latitude, point.longitude, point.speed]]
    prediction = saved_model.predict(input_data)
    is_anomaly = bool(prediction[0] == -1)
    
    # If anomaly detected, simulate sending an SMS alert
    if is_anomaly:
        send_alert_sms(point.latitude, point.longitude)
    
    return {
        "is_anomaly": is_anomaly,
        "message": "Unusual movement detected!" if is_anomaly else "Movement looks normal"
    }


def send_alert_sms(latitude, longitude):
    """
    Simulates sending an emergency SMS alert to family contacts.
    In a production deployment, this would use Twilio's API to send
    a real SMS. For this prototype, we log the alert to demonstrate
    the alerting logic and message content.
    """
    message = (
        f"SafeHer ALERT: Unusual movement detected!\n"
        f"Location: https://maps.google.com/?q={latitude},{longitude}\n"
        f"Please check on your contact immediately."
    )
    
    print("=" * 50)
    print("EMERGENCY SMS ALERT TRIGGERED")
    print(message)
    print("=" * 50)
    
    # ===== Real Twilio integration would look like this: =====
    # from twilio.rest import Client
    # client = Client(ACCOUNT_SID, AUTH_TOKEN)
    # client.messages.create(
    #     body=message,
    #     from_=TWILIO_PHONE_NUMBER,
    #     to=FAMILY_CONTACT_NUMBER
    # )