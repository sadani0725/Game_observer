import cv2
import numpy as np

def detect_hp_ratio(frame):

    hp_region = frame[76:87, 194:441]
    hsv = cv2.cvtColor(hp_region, cv2.COLOR_BGR2HSV)

    # piros szín maszk
    mask1 = cv2.inRange(hsv, (0, 70, 70), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 70, 70), (180, 255, 255))
    mask = mask1 | mask2

    ratio = np.sum(mask > 0) / mask.size
    return ratio