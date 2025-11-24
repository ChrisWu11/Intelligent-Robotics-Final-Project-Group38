def detect_red_zone(rgb):
    red = rgb[:, :, 0]
    green = rgb[:, :, 1]
    blue = rgb[:, :, 2]

    mask = (red > 140) & (green < 110) & (blue < 110)

    count = mask.sum()

    return count > 1500  # threshold depends on your camera FOV
