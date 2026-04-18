import cv2
import os

# -------- CONFIG --------
CASCADE_PATH = "models/face/haarcascade_frontalface_default.xml"
IMG_SIZE = 224
# ------------------------

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

if face_cascade.empty():
    raise ValueError("Haar cascade not loaded. Check CASCADE_PATH.")

def crop_face(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    if len(faces) == 0:
        face = img
    else:
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        m = int(0.3 * w)
        face = img[
            max(0, y - m): y + h + m,
            max(0, x - m): x + w + m
        ]

    face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))

    out_path = image_path.replace(".jpg", "_face.jpg")
    cv2.imwrite(out_path, face)

    return out_path
