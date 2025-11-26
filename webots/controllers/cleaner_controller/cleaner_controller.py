from controller import Robot, Camera, Motor
from perception import detect_red_zone
from navigation import avoid_obstacles, forward
from behavior_fsm import BehaviorFSM

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
left_motor.setVelocity(0)
right_motor.setVelocity(0)

# FSM
fsm = BehaviorFSM()

# Cooldown: prevents repeated CLEAN triggers
clean_cooldown = 0.0    # seconds

print("Python cleaner_controller started.")

while robot.step(TIME_STEP) != -1:

    # Cooldown countdown
    if clean_cooldown > 0:
        clean_cooldown -= TIME_STEP / 1000.0

    ### 1. Read camera ###
    image = camera.getImage()
    if image is None:
        print("Camera not ready")
        continue

    ### 2. Perception ###
    red_detected = detect_red_zone(camera, image)
    print("Red zone detected:", red_detected)

    ### 3. Update FSM ###
    # Only allow red→CLEAN if cooldown has expired
    if red_detected and clean_cooldown <= 0:
        fsm.update(True)
    else:
        fsm.update(False)

    state = fsm.state
    print("FSM State:", state)

    ### 4. Execute state behaviour ###
    if state == "EXPLORE":
        avoid_obstacles(robot, left_motor, right_motor)

    elif state == "CLEAN":
        print("=== ENTER CLEAN MODE ===")

        # Step 1: Move forward for 2 seconds
        start = robot.getTime()
        while robot.getTime() - start < 2.0:
            left_motor.setVelocity(3.0)
            right_motor.setVelocity(3.0)
            robot.step(TIME_STEP)

        # Step 2: Stop for 3 seconds (simulate cleaning)
        start = robot.getTime()
        print("[CLEANING] Stopping for 3 seconds…")
        while robot.getTime() - start < 3.0:
            left_motor.setVelocity(0)
            right_motor.setVelocity(0)
            robot.step(TIME_STEP)

        # Step 3: Rotate 180 degrees
        print("[ROTATE] Turning 180 degrees")
        left_motor.setVelocity(3.0)
        right_motor.setVelocity(-3.0)
        robot.step(900)   # tune if needed

        print("=== CLEAN CYCLE COMPLETE ===")

        # Step 4: Apply cooldown to avoid instant re-trigger
        clean_cooldown = 5.0   # seconds

        # Step 5: Return to EXPLORE mode
        fsm.state = "EXPLORE"
        continue

    else:
        forward(left_motor, right_motor)
