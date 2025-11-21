import cv2
import numpy as np

class Vision:
    def __init__(self, robot):
        self.cam = robot.getDevice('camera')
        self.cam.enable(64)

    def detects_red(self):
        image = self.cam.getImageArray()
        if image is None:
            return False
        img = np.array(image, dtype=np.uint8)
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        lower = np.array([0, 120, 70])
        upper = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        return np.sum(mask) > 500
