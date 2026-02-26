# FastAPI application to serve logged timestamps
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import os

app = FastAPI() #creates instance

# Read log file path from environment 
DATA_FILE = os.environ.get("DATA_FILE", "/data/timestamps.log")

# Health check endpoint (not yet used in K8s, but can be called manually by curl http://localhost:8080/health)
@app.get("/health")
def health():
    return {"status": "ok"}

# Return last N timestamps from log
@app.get("/outputs")
def outputs(limit: int = Query(10, ge=1, le=1000)):
    items = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f: #encoding for consistency across environments
            # Filter empty lines and clean up line endings
            lines = [line.rstrip("\n") for line in f.readlines() if line.strip()]

        # Get last N items in JSON format
        items = lines[-limit:]
    return JSONResponse({"count": len(items), "items": items})