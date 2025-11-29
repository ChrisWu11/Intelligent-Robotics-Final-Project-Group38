from controller import Robot, Camera, Motor
from perception import detect_red_zone
from navigation import avoid_obstacles, forward
from behavior_fsm import BehaviorFSM
import json

TIME_STEP = 32
robot = Robot()

# Camera
camera = robot.getDevice("camera")
camera.enable(TIME_STEP)

# Motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

fsm = BehaviorFSM()

# Cooldown timer
clean_cooldown = 0.0

def write_state_to_file(state):
    """让 supervisor 能够知道当前是否在 CLEAN 状态"""
    with open("/tmp/robot_state.json", "w") as f:
        json.dump({"state": state}, f)

print("Python cleaner_controller started.")

while robot.step(TIME_STEP) != -1:

    if clean_cooldown > 0:
        clean_cooldown -= TIME_STEP / 1000.0

    image = camera.getImage()
    if image is None:
        continue

    red_detected = detect_red_zone(camera, image)

    if red_detected and clean_cooldown <= 0:
        fsm.update(True)
    else:
        fsm.update(False)

    state = fsm.state
    write_state_to_file(state)

    if state == "EXPLORE":
        avoid_obstacles(robot, left_motor, right_motor)

    elif state == "CLEAN":
        print("=== ENTER CLEAN MODE ===")

        # Move forward into the zone
        start = robot.getTime()
        while robot.getTime() - start < 2.0:
            forward(left_motor, right_motor, speed=5.0)
            robot.step(TIME_STEP)

        # Cleaning pause
        start = robot.getTime()
        while robot.getTime() - start < 3.0:
            left_motor.setVelocity(0)
            right_motor.setVelocity(0)
            robot.step(TIME_STEP)

        # turn
        left_motor.setVelocity(5.0)
        right_motor.setVelocity(-2.5)
        robot.step(900)

        clean_cooldown = 4.0
        fsm.state = "EXPLORE"

    else:
        forward(left_motor, right_motor)
