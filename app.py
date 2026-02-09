# app.py
from fastapi import FastAPI, HTTPException, Request
import redis
import os
from pydantic import BaseModel

app = FastAPI()

# Read environment variables (Docker/K8s friendly)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Initialize Redis client
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True  # returns strings instead of bytes
)

# Middleware to log incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# Pydantic model for POST requests
class CacheItem(BaseModel):
    key: str
    value: str

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI + Redis app!"}

# Get value from Redis
@app.get("/cache")
def get_value(key: str):
    value = r.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}

# Set value in Redis
@app.post("/cache")
def set_value(item: CacheItem):
    r.set(item.key, item.value)
    return {"message": f"Stored key '{item.key}' successfully."}

# Show Redis password (for testing only, remove in production!)
@app.get("/secret-test")
def show_secret():
    return {"password": REDIS_PASSWORD}
