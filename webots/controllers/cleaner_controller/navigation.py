# navigation.py

FORWARD_SPEED = 5.0
TURN_SPEED = 3.5

initialized = False
sensors = []

TIME_STEP = 32   # 加这个即可


def init_obstacle_sensors(robot):
    global initialized, sensors

    if initialized:
        return

    sensor_names = ["ps0", "ps1", "ps2", "ps3", "ps4", "ps5", "ps6", "ps7"]

    for name in sensor_names:
        s = robot.getDevice(name)
        s.enable(TIME_STEP)     # ← FIXED!
        sensors.append(s)

    initialized = True
    print("[NAV] Proximity sensors initialized.")


def forward(left_motor, right_motor, speed=FORWARD_SPEED):
    left_motor.setVelocity(speed)
    right_motor.setVelocity(speed)


def avoid_obstacles(robot, left_motor, right_motor):
    init_obstacle_sensors(robot)

    values = [s.getValue() for s in sensors]

    threshold = 80

    right_hit = values[0] > threshold or values[1] > threshold or values[2] > threshold
    left_hit = values[5] > threshold or values[6] > threshold or values[7] > threshold

    if left_hit:
        left_motor.setVelocity(TURN_SPEED)
        right_motor.setVelocity(-TURN_SPEED)

    elif right_hit:
        left_motor.setVelocity(-TURN_SPEED)
        right_motor.setVelocity(TURN_SPEED)

    else:
        forward(left_motor, right_motor)
