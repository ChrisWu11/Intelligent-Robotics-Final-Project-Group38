import numpy as np
import cv2

def detect_red_zone(camera, raw_image):
    width = camera.getWidth()
    height = camera.getHeight()

    # Convert Webots buffer → numpy array
    img = np.frombuffer(raw_image, dtype=np.uint8).reshape((height, width, 4))
    img = img[:, :, :3]  # remove alpha

    # Convert BGR → RGB → HSV
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # 1. Red mask (rough detection)
    mask1 = cv2.inRange(hsv, (0, 100, 80), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 100, 80), (180, 255, 255))
    mask = mask1 | mask2

    # Ratio of red pixels
    red_ratio = np.sum(mask > 0) / (width * height)

    # If red area is tiny → ignore
    if red_ratio < 0.05:   # 5% of camera frame
        return False

    # 2. Edge detection
    edges = cv2.Canny(mask, 50, 150)

    edge_ratio = np.sum(edges > 0) / (width * height)

    # 3. Color consistency check
    red_pixels = hsv[:, :, 2][mask > 0]   # V channel
    brightness_var = np.var(red_pixels)

    # Debug info
    print(f"Red ratio: {red_ratio:.3f}, Edge ratio: {edge_ratio:.3f}, Var: {brightness_var:.1f}")

    # 4. Intelligent decision
    if red_ratio > 0.10 and edge_ratio < 0.05 and brightness_var < 400:
        # 明显是一大片红色表面
        print("[AI DETECT] Large red zone detected.")
        return True

    return False
