from ultralytics import YOLO
import cv2
import datetime
import os
import time
from alert import send_all_alerts

# ── Model ─────────────────────────────────────────────────────────────────────
# YOLOv8n downloads automatically on first run (~6 MB)
model = YOLO('yolov8n.pt')

# ── Animal class IDs (COCO dataset) ───────────────────────────────────────────
ANIMAL_CLASSES = {
    14: "bird",
    15: "cat",   16: "dog",      17: "horse",  18: "sheep",
    19: "cow",   20: "elephant", 21: "bear",
    22: "zebra", 23: "giraffe"
}

# ── Cooldown: only alert once per animal per N seconds ────────────────────────
ALERT_COOLDOWN = 60          # seconds between alerts for the same animal
last_alert: dict[str, float] = {}

os.makedirs("logs", exist_ok=True)

cap = cv2.VideoCapture(0)   # 0 = default webcam
if not cap.isOpened():
    print("❌ Cannot open camera. Check that a webcam is connected.")
    exit(1)

print("✅ Farm Monitor Started — press Q to quit")
print(f"⏱  Alert cooldown: {ALERT_COOLDOWN}s per animal")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️  Frame read failed. Retrying...")
        time.sleep(0.1)
        continue

    results = model(frame, verbose=False)

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            if class_id not in ANIMAL_CLASSES:
                continue

            animal_name = ANIMAL_CLASSES[class_id]
            now         = time.time()

            # Skip if we alerted for this animal too recently
            if now - last_alert.get(animal_name, 0) < ALERT_COOLDOWN:
                continue

            last_alert[animal_name] = now
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Save snapshot
            img_path = f"logs/{animal_name}_{timestamp}.jpg"
            cv2.imwrite(img_path, frame)

            print(f"🚨 {animal_name.upper()} detected at {timestamp}!")
            send_all_alerts(animal_name, timestamp, img_path)

    # Show live annotated feed
    annotated_frame = results[0].plot()
    if annotated_frame is not None:
        cv2.imshow('🌾 Farm Animal Monitor  [Q = quit]', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("👋 Farm Monitor stopped.")