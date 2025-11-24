def avoid_obstacle(ps):
    values = [s.getValue() for s in ps]

    left_blocked = values[0] > 80 or values[1] > 80
    right_blocked = values[6] > 80 or values[7] > 80

    if left_blocked:
        return -3.0, 3.0  # turn right
    if right_blocked:
        return 3.0, -3.0  # turn left

    return 3.0, 3.0  # forward
