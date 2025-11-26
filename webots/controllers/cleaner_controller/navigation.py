def forward(left_motor, right_motor, speed=4.0):
    left_motor.setVelocity(speed)
    right_motor.setVelocity(speed)

def avoid_obstacles(robot, left_motor, right_motor):
    # Placeholder: always move forward for now
    left_motor.setVelocity(3.5)
    right_motor.setVelocity(3.5)
