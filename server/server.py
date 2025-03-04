from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import sqlite3
import json
import asyncio
import hashlib
import uvicorn
import pandas as pd

active_connections = set()
last_data_hash = None  # Store the last sent hash


async def broadcast_message(data):
    """Send updates to all active WebSocket clients."""
    if active_connections:  # Only send if there are active connections
        await asyncio.gather(*(connection.send_json(data) for connection in active_connections))


# Get the latest assessment data
def get_latest_assessments():
    # TODO: use real time data from database
    df = pd.read_csv("random_points.csv")
    
    df['Average Score'] = df[df.columns[4:]].mean(axis=1)
    
    mapper = {
        "point_id": "ID", 
        "lat": "Latitude", 
        "lon": "Longitude",
        "Average Score": "Score"
    }
    
    return df[mapper.keys()].rename(columns=mapper).to_dict(orient="records")
    
    
    
# Compute an average score from JSON data
def compute_avg_score(data):
    # TODO: code
    ...


def compute_data_hash(data):
    """Generate a hash of the dataset for change detection."""
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode()).hexdigest()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function to start background tasks."""
    task = asyncio.create_task(data_update_task())  # Start background task
    yield
    task.cancel()  # Cancel task on shutdown


app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections."""
    await websocket.accept()
    active_connections.add(websocket)

    try:
        # 🔹 Send latest data immediately upon connection
        latest_data = get_latest_assessments()
        await websocket.send_json(latest_data)

        while True:
            await websocket.receive_text()  # Keep WebSocket alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        
@app.get("/points", response_class=JSONResponse)
async def get_points():
    """GET endpoint to fetch the latest assessment data as JSON."""
    data = get_latest_assessments()
    return JSONResponse(content=data)  # Explicitly return JSON

async def data_update_task():
    """Background task that fetches and sends updates only when needed."""
    global last_data_hash

    while True:
        data = get_latest_assessments()
        current_hash = compute_data_hash(data)

        if current_hash != last_data_hash:
            last_data_hash = current_hash  # Store new hash
            await broadcast_message(data)  # Send updates to all clients

        await asyncio.sleep(5)  # Send updates every 5 seconds

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8472)