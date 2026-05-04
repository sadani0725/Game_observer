import cv2
import numpy as np

def calculate_hp(strict_roi):
    roi = strict_roi

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower1 = np.array([0, 70, 50])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 70, 50])
    upper2 = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)

    filled = cv2.countNonZero(mask)
    total = roi.shape[0] * roi.shape[1]

    if total == 0:
        return None

    return round((filled / total) * 100, 1)/100