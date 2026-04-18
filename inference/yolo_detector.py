from ultralytics import YOLO
import cv2

yolo_model = YOLO("models/yolo/best.pt")

def get_yolo_roi(image, selected_concern=None):
    results = yolo_model(image)

    best_roi = None
    max_area = 0

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)

            roi = image[y1:y2, x1:x2]

            if roi.size == 0:
                continue

            area = (x2 - x1) * (y2 - y1)

            if area > max_area:
                max_area = area
                best_roi = roi

    return best_roi