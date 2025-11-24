from controller import Robot, Camera
import numpy as np

from navigation import avoid_obstacle
from perception import detect_red_zone
from behavior_fsm import FSM

TIME_STEP = 64

robot = Robot()

# Motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0)
right_motor.setVelocity(0)

# IR sensors
ps = []
for i in range(8):
    sensor = robot.getDevice(f"ps{i}")
    sensor.enable(TIME_STEP)
    ps.append(sensor)

# Camera
camera = robot.getDevice("camera")
camera.enable(TIME_STEP)

# FSM instance
fsm = FSM()

print(f"Initial state: {fsm.state}")

while robot.step(TIME_STEP) != -1:

    # --- 1. Get camera image and detect red zone ---
    image = camera.getImage()
    red_detected = False

    if image:
        img = np.frombuffer(image, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
        rgb = img[:, :, :3]
        red_detected = detect_red_zone(rgb)

    # --- 2. State transition ---
    fsm.update(red_detected)

    # --- 3. Act according to state ---
    if fsm.state == "explore":
        vl, vr = avoid_obstacle(ps)

    elif fsm.state == "focused_cleaning":
        vl, vr = 1.5, 1.5  # slow sweeping behavior

    elif fsm.state == "avoid":
        vl, vr = -2.0, 2.0

    # --- 4. Send motor commands ---
    left_motor.setVelocity(vl)
    right_motor.setVelocity(vr)
