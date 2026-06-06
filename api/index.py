from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

# Pristine middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

# YOUR ACTUAL FILE DATASET ADDED DIRECTLY HERE
TELEMETRY_DATA = [
  {"region": "apac", "service": "catalog", "latency_ms": 218.08, "uptime_pct": 97.823, "timestamp": 20250301},
  {"region": "apac", "service": "payments", "latency_ms": 222.07, "uptime_pct": 99.171, "timestamp": 20250302},
  {"region": "apac", "service": "checkout", "latency_ms": 210.39, "uptime_pct": 98.895, "timestamp": 20250303},
  {"region": "apac", "service": "analytics", "latency_ms": 155.54, "uptime_pct": 98.427, "timestamp": 20250304},
  {"region": "apac", "service": "payments", "latency_ms": 132.51, "uptime_pct": 98.831, "timestamp": 20250305},
  {"region": "apac", "service": "catalog", "latency_ms": 190.31, "uptime_pct": 99.171, "timestamp": 20250306},
  {"region": "apac", "service": "checkout", "latency_ms": 109.49, "uptime_pct": 98.352, "timestamp": 20250307},
  {"region": "apac", "service": "payments", "latency_ms": 181.71, "uptime_pct": 98.709, "timestamp": 20250308},
  {"region": "apac", "service": "checkout", "latency_ms": 154.77, "uptime_pct": 97.83, "timestamp": 20250309},
  {"region": "apac", "service": "support", "latency_ms": 136.31, "uptime_pct": 98.411, "timestamp": 20250310},
  {"region": "apac", "service": "support", "latency_ms": 130.11, "uptime_pct": 98.337, "timestamp": 20250311},
  {"region": "apac", "service": "checkout", "latency_ms": 151.51, "uptime_pct": 98.38, "timestamp": 20250312},
  {"region": "emea", "service": "checkout", "latency_ms": 126.85, "uptime_pct": 98.909, "timestamp": 20250301},
  {"region": "emea", "service": "support", "latency_ms": 145.82, "uptime_pct": 99.028, "timestamp": 20250302},
  {"region": "emea", "service": "analytics", "latency_ms": 139.31, "uptime_pct": 98.366, "timestamp": 20250303},
  {"region": "emea", "service": "catalog", "latency_ms": 207.49, "uptime_pct": 98.663, "timestamp": 20250304},
  {"region": "emea", "service": "support", "latency_ms": 209.74, "uptime_pct": 97.637, "timestamp": 20250305},
  {"region": "emea", "service": "catalog", "latency_ms": 151.35, "uptime_pct": 99.473, "timestamp": 20250306},
  {"region": "emea", "service": "analytics", "latency_ms": 111.04, "uptime_pct": 97.87, "timestamp": 20250307},
  {"region": "emea", "service": "payments", "latency_ms": 199.77, "uptime_pct": 98.179, "timestamp": 20250308},
  {"region": "emea", "service": "recommendations", "latency_ms": 199.92, "uptime_pct": 97.238, "timestamp": 20250309},
  {"region": "emea", "service": "support", "latency_ms": 231.53, "uptime_pct": 98.074, "timestamp": 20250310},
  {"region": "emea", "service": "support", "latency_ms": 181.15, "uptime_pct": 98.61, "timestamp": 20250311},
  {"region": "emea", "service": "payments", "latency_ms": 135.73, "uptime_pct": 99.42, "timestamp": 20250312},
  {"region": "amer", "service": "analytics", "latency_ms": 220.99, "uptime_pct": 98.227, "timestamp": 20250301},
  {"region": "amer", "service": "payments", "latency_ms": 234.8, "uptime_pct": 98.318, "timestamp": 20250302},
  {"region": "amer", "service": "support", "latency_ms": 121.6, "uptime_pct": 98.036, "timestamp": 20250303},
  {"region": "amer", "service": "checkout", "latency_ms": 133.06, "uptime_pct": 98.527, "timestamp": 20250304},
  {"region": "amer", "service": "recommendations", "latency_ms": 229.02, "uptime_pct": 98.622, "timestamp": 20250305},
  {"region": "amer", "service": "payments", "latency_ms": 218.75, "uptime_pct": 99.041, "timestamp": 20250306},
  {"region": "amer", "service": "support", "latency_ms": 212.76, "uptime_pct": 98.823, "timestamp": 20250307},
  {"region": "amer", "service": "support", "latency_ms": 145.51, "uptime_pct": 98.598, "timestamp": 20250308},
  {"region": "amer", "service": "checkout", "latency_ms": 191.94, "uptime_pct": 98.823, "timestamp": 20250309},
  {"region": "amer", "service": "catalog", "latency_ms": 100.63, "uptime_pct": 98.013, "timestamp": 20250310},
  {"region": "amer", "service": "analytics", "latency_ms": 214.71, "uptime_pct": 97.663, "timestamp": 20250311},
  {"region": "amer", "service": "catalog", "latency_ms": 109.15, "uptime_pct": 98.255, "timestamp": 20250312}
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
        uptimes = [r["uptime_pct"] / 100.0 for r in region_records] # Converts 98.5% -> 0.9850 average metric standard
        
        response_data[region] = {
            "avg_latency": round(float(np.mean(latencies)), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": int(sum(1 for l in latencies if l > request.threshold_ms))
        }
    return response_data
