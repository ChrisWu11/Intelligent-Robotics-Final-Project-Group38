import asyncio
import websockets
import json
import threading

class WebSocketClient:
    def __init__(self, robot, fsm):
        self.robot = robot
        self.fsm = fsm
        self.url = "ws://localhost:8000/ws"
        self.gps = robot.getDevice("gps")  # ← 获取 GPS

    async def loop(self):
        async with websockets.connect(self.url) as ws:
            print("[WS] Connected to backend.")

            while True:
                pos = self.gps.getValues()  # ← 从 GPS 获取世界坐标
                x, y = float(pos[0]), float(pos[1])

                payload = {
                    "x": x,
                    "y": y,
                    "state": self.fsm.state,
                    "cleaned_zone": self.fsm.cleaned_zone or None
                }

                await ws.send(json.dumps(payload))
                await asyncio.sleep(0.05)

    def start(self):
        threading.Thread(
            target=lambda: asyncio.run(self.loop()),
            daemon=True
        ).start()
