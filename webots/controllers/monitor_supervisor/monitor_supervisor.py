from controller import Supervisor
import websocket
import json
import threading
import time
import os

robot = Supervisor()
TIME_STEP = int(robot.getBasicTimeStep())

epuck = robot.getFromDef("CLEANER")
trans = epuck.getField("translation")

STATE_FILE = "/tmp/robot_state.json"
previous_clean_state = False

def ws_sender():
    ws = None

    while True:
        try:
            if ws is None:
                print("[WS] Connecting to backend...")
                ws = websocket.WebSocket()
                ws.connect("ws://localhost:8765/ws/supervisor")
                print("[WS] Connected!")

            while True:
                pos = trans.getSFVec3f()
                msg = {
                    "event": "position",
                    "x": pos[0],
                    "y": pos[1]
                }
                ws.send(json.dumps(msg))

                # Detect CLEAN state
                global previous_clean_state
                if os.path.exists(STATE_FILE):
                    with open(STATE_FILE) as f:
                        state_json = json.load(f)
                        state = state_json.get("state", "EXPLORE")

                        if state == "CLEAN" and previous_clean_state == False:
                            # First frame of CLEAN = zone cleaned
                            clean_msg = {
                                "event": "cleaned",
                                "x": pos[0],
                                "y": pos[1]
                            }
                            ws.send(json.dumps(clean_msg))
                            print("[WS] Cleaned zone sent:", clean_msg)

                            previous_clean_state = True

                        if state != "CLEAN":
                            previous_clean_state = False

                time.sleep(0.1)

        except Exception as e:
            print("[WS ERROR]", e)
            ws = None
            time.sleep(1)

# background websocket thread
threading.Thread(target=ws_sender, daemon=True).start()

# normal supervisor loop
while robot.step(TIME_STEP) != -1:
    pass
