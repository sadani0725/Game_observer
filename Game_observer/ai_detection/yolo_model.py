from ultralytics import YOLO

model = YOLO("Game_observer/models/YOLO/best.pt")

def predict(frame, conf=0.50):
    results = model(frame, conf=conf)
    return results[0]