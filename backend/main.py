from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

active_clients = []
active_supervisors = []
cleaned_zones = set()

@app.websocket("/ws")
async def websocket_frontend(websocket: WebSocket):
    await websocket.accept()
    active_clients.append(websocket)
    print("[WS] Frontend connected.")

    try:
        while True:
            # 前端一般不会发消息，这里只是防掉线
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
            print('msg',msg)
            # 广播 supervisor 坐标到前端
            for c in active_clients:
                await c.send_text(json.dumps({
                    "supervisor_x": msg["x"],
                    "supervisor_y": msg["y"]
                }))

    except WebSocketDisconnect:
        active_supervisors.remove(websocket)
        print("[WS] Supervisor disconnected.")