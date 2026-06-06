from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

# Let FastAPI handle the layer middleware purely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

TELEMETRY_DATA = [
    {"region": "apac", "latency_ms": 120.5, "uptime": 1},
    {"region": "apac", "latency_ms": 195.2, "uptime": 1},
    {"region": "apac", "latency_ms": 85.0, "uptime": 0},
    {"region": "amer", "latency_ms": 150.0, "uptime": 1},
    {"region": "amer", "latency_ms": 210.4, "uptime": 1},
    {"region": "amer", "latency_ms": 110.1, "uptime": 1}
]

class AnalyticsRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

@app.get("/")
def home():
    return {"status": "healthy"}

@app.post("/")
def calculate_metrics(request: AnalyticsRequest):
    response_data = {}
    for region in request.regions:
        clean_region = str(region).strip().lower()
        region_records = [r for r in TELEMETRY_DATA if r["region"].lower() == clean_region]
        
        if not region_records:
            response_data[region] = {"avg_latency": 0.0, "p95_latency": 0.0, "avg_uptime": 0.0, "breaches": 0}
            continue
            
        latencies = [r["latency_ms"] for r in region_records]
        uptimes = [r["uptime"] for r in region_records]
        
        response_data[region] = {
            "avg_latency": round(float(np.mean(latencies)), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": int(sum(1 for l in latencies if l > request.threshold_ms))
        }
    return response_data
