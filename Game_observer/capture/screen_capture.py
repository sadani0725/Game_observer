import mss
import numpy as np
import cv2

def capture_frame():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # fő monitor
        frame = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame