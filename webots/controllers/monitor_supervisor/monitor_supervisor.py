from controller import Supervisor
import websocket
import json
import threading
import time

robot = Supervisor()
TIME_STEP = int(robot.getBasicTimeStep())

# Locate robot
epuck = robot.getFromDef("CLEANER")
trans = epuck.getField("translation")

# Create websocket connection
def ws_sender():
    ws = None

    while True:
        try:
            if ws is None:
                print("[WS] Connecting to backend...")
                ws = websocket.WebSocket()
                ws.connect("ws://localhost:8765/ws/supervisor")
                print("[WS] Connected!")

            # send loop
            while True:
                pos = trans.getSFVec3f()
                rot = epuck.getField("rotation").getSFRotation()

                msg = {
                    "event": "position",
                    "x": pos[0],
                    "y": pos[1],
                    "z": pos[2],
                    "ry": rot[3]
                }

                ws.send(json.dumps(msg))
                time.sleep(0.1)

        except Exception as e:
            print("[WS ERROR]", e)
            ws = None
            time.sleep(1)  # retry after 1s


# Start WebSocket thread
threading.Thread(target=ws_sender, daemon=True).start()

# Normal Webots step loop
while robot.step(TIME_STEP) != -1:
    pass
