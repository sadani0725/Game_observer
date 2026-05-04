def extract_bar_strip(frame, box):
    x1, y1, x2, y2 = box

    h = y2 - y1
    thin = int(h * 0.2)  # 20% height

    y_center = y1 + h // 2
    y_start = max(y_center - thin // 2, 0)
    y_end = min(y_center + thin // 2, frame.shape[0])

    return frame[y_start:y_end, x1:x2]