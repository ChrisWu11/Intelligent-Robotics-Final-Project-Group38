from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

active_clients = []
active_supervisors = []
cleaned_zones = []

@app.websocket("/ws")
async def websocket_frontend(websocket: WebSocket):
    await websocket.accept()
    active_clients.append(websocket)
    print("[WS] Frontend connected.")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        active_clients.remove(websocket)
        print("[WS] Frontend disconnected.")

@app.websocket("/ws/supervisor")
async def websocket_supervisor(websocket: WebSocket):
    await websocket.accept()
    active_supervisors.append(websocket)
    print("[WS] Supervisor connected.")

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            if msg["event"] == "position":
                for c in active_clients:
                    await c.send_text(json.dumps({
                        "type": "position",
                        "x": msg["x"],
                        "y": msg["y"]
                    }))

            elif msg["event"] == "cleaned":
                cleaned_zones.append({"x": msg["x"], "y": msg["y"]})
                for c in active_clients:
                    await c.send_text(json.dumps({
                        "type": "cleaned_zone",
                        "zones": cleaned_zones
                    }))

    except WebSocketDisconnect:
        active_supervisors.remove(websocket)
        print("[WS] Supervisor disconnected.")
