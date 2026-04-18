import cv2
import numpy as np
from keras.models import load_model
from keras.applications.mobilenet_v2 import preprocess_input

from inference.face_crop import crop_face
from inference.yolo_detector import get_yolo_roi

# CONFIG
MODEL_PATH = "models/efficientnet/skin_classifier.keras"
IMG_SIZE = 224

CLASS_NAMES = [
    "acne",
    "blackheads",
    "dryness",
    "enlarged_pores",
    "hyperpigmentation",
    "redness"
]

# LOAD MODEL
print("Loading classifier model...")
model = load_model(MODEL_PATH, compile=False)
print("Model loaded successfully")


# PREPROCESS
def preprocess_image(img):
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = np.array(img, dtype=np.float32)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img


# MAIN PREDICTION
def predict_from_images(image_paths, selected_concern):

    rois = []

    # SAFE CLASS INDEX
    try:
        class_index = CLASS_NAMES.index(selected_concern)
    except ValueError:
        print(f"Unknown concern: {selected_concern}, defaulting to acne")
        class_index = 0
        selected_concern = "acne"

    # STEP 1: FACE + YOLO
    for path in image_paths:
        try:
            face_path = crop_face(path)
            img = cv2.imread(face_path)

            if img is None:
                continue

            roi = get_yolo_roi(img, selected_concern)

            if roi is not None and roi.size > 0:
                rois.append(roi)

        except Exception as e:
            print("Error:", e)

    # STEP 2: FALLBACK
    if len(rois) == 0:
        print("YOLO failed → fallback to face")

        for p in image_paths:
            try:
                face = cv2.imread(crop_face(p))

                if face is not None:
                    rois.append(face)

            except Exception as e:
                print("Fallback error:", e)

    # STEP 3: PREDICTION
    confidences = []

    for roi in rois:
        try:
            img = preprocess_image(roi)

            pred = model.predict(img, verbose=0)

            # SAFE CHECK
            if pred is None or len(pred) == 0:
                continue

            pred = pred[0]

            if len(pred) <= class_index:
                print("Prediction size mismatch:", pred.shape)
                continue

            confidences.append(float(pred[class_index]))

        except Exception as e:
            print("Prediction error:", e)

    # STEP 4: FINAL SAFETY
    if len(confidences) == 0:
        print("No valid predictions")
        return selected_concern, "Mild", 0.1

    avg_conf = float(np.mean(confidences))

    # STEP 5: SEVERITY
    if avg_conf > 0.7:
        severity = "Severe"
    elif avg_conf > 0.4:
        severity = "Moderate"
    else:
        severity = "Mild"

    return selected_concern, severity, round(avg_conf, 4)