import cv2
import numpy as np

def calculate_stamina(strict_roi):
    roi = strict_roi

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower1 = np.array([35, 70, 50])
    upper1 = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower1, upper1)

    filled = cv2.countNonZero(mask)
    total = roi.shape[0] * roi.shape[1]

    if total == 0:
        return None

    return round((filled / total) * 100, 1)/100