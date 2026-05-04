import cv2
import os

# BEÁLLÍTÁSOK

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(BASE_DIR, "videos", "gameplay1.mp4")

OUTPUT = os.path.join(BASE_DIR, "extracted_pics")

FRAME_EVERY_N = 60     
MAX_FRAMES = 500        

# MAPPÁK LÉTREHOZÁSA
os.makedirs(OUTPUT, exist_ok=True)

# VIDEÓ MEGNYITÁSA
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f"Error: Could not open video: {VIDEO_PATH}")
    exit()

frame_count = 0
saved_count = 0

print("Frame extraction starting...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % FRAME_EVERY_N == 0:

        filename = f"frame_{saved_count:05d}.jpg"
        output_path = os.path.join(OUTPUT, filename)

        success, encoded_image = cv2.imencode(".jpg", frame)
        if success:
            encoded_image.tofile(output_path)
            print(f"[OK] Saved: {output_path}")
        else:
            print(f"[Error] Could not save: {output_path}")

        saved_count += 1

        if MAX_FRAMES is not None and saved_count >= MAX_FRAMES:
            break

    frame_count += 1

cap.release()

print(f"Done. All saved frames: {saved_count}")