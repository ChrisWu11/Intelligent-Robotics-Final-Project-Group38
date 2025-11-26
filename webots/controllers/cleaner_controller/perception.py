import numpy as np
import cv2

def detect_red_zone(camera, raw_image):
    width = camera.getWidth()
    height = camera.getHeight()

    # Convert Webots buffer → numpy array
    img = np.frombuffer(raw_image, dtype=np.uint8).reshape((height, width, 4))
    img = img[:, :, :3]  # Remove alpha

    # Convert BGR → RGB → HSV
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Red mask (two ranges)
    mask1 = cv2.inRange(hsv, (0, 100, 80), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 100, 80), (180, 255, 255))
    mask = mask1 | mask2

    # Canny edges
    edges = cv2.Canny(mask, 50, 150)

    # Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check large region
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 400:  # threshold
            print("Red region detected, area:", area)
            return True

    return False
