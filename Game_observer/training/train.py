from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="training/dataset/data.yaml",
    epochs=50,
    imgsz=960,
    batch=8,
    name="ui_detector"
)