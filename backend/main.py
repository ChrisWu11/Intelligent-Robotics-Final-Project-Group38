from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

active_clients = []
cleaned_zones = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_clients.append(websocket)
    print("[WS] client connected.")

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            # 如果 controller 上传 cleaned_zone
            if msg.get("cleaned_zone") is not None:
                cleaned_zones.add(msg["cleaned_zone"])

            # 广播
            for client in active_clients:
                await client.send_text(json.dumps({
                    "x": msg["x"],
                    "y": msg["y"],
                    "state": msg["state"],
                    "cleaned_zones": list(cleaned_zones)
                }))

    except WebSocketDisconnect:
        active_clients.remove(websocket)
        print("[WS] client disconnected.")
