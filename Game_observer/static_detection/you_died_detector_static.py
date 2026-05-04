import cv2

def detect_you_died(frame, template_path="Game_observer/Templates/you_died_template.png", threshold=0.8):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = (res >= threshold).any()
    return loc
