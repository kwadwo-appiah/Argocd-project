from fastapi import FastAPI, HTTPException, Request
import redis
import os
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, start_http_server
from fastapi.responses import Response

app = FastAPI(title="Python FastAPI + Redis App with Metrics")

# -------------------------------
# Prometheus Metrics
# -------------------------------
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests received",
    ["method", "endpoint"]
)

# -------------------------------
# Redis connection
# -------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

# -------------------------------
# Middleware to count requests
# -------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    return response

# -------------------------------
# API Endpoints
# -------------------------------
@app.get("/")
def root():
    return {"message": "FastAPI is working"}

@app.post("/cache")
def store_value(key: str, value: str):
    r.set(key, value)
    return {"message": f"Stored key '{key}'"}

@app.get("/cache")
def get_value(key: str):
    value = r.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value.decode()}

# -------------------------------
# Metrics Endpoint
# -------------------------------
@app.on_event("startup")
async def startup_event():
    # This creates a separate background thread listening on 8001
    # Prometheus will now find your metrics here.
    metrics_port = 8001
    start_http_server(metrics_port)
    print(f"--- Metrics server started on port {metrics_port} ---")

# -------------------------------
# Main API Endpoints (on Port 8000)
# -------------------------------
@app.get("/")
def root():
    return {"message": "FastAPI is working on port 8000"}

# Note: You can remove the @app.get("/metrics") from the FastAPI app
# if you want port 8000 to remain strictly for the API.
# -------------------------------
# Optional: secret test
# -------------------------------
@app.get("/secret-test")
def show_secret():
    return {"password": os.getenv("REDIS_PASSWORD")}
