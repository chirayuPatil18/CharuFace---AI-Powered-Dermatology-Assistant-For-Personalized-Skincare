import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# CONFIG
MODEL_PATH = "models/efficientnet/skin_classifier.keras"
TEST_DIR = "training/dataset/cnn_dataset/test"
IMG_SIZE = (224, 224)

# LOAD MODEL
print("Loading model...")
model = load_model(MODEL_PATH)

class_names = sorted(os.listdir(TEST_DIR))

# EVALUATION
correct = 0
total = 0

print("\nRunning system-level evaluation...\n")

for class_idx, class_name in enumerate(class_names):
    class_path = os.path.join(TEST_DIR, class_name)

    for img_file in os.listdir(class_path):
        img_path = os.path.join(class_path, img_file)

        try:
            img = image.load_img(img_path, target_size=IMG_SIZE)
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            pred = model.predict(img_array, verbose=0)
            pred_class = np.argmax(pred)

            if pred_class == class_idx:
                correct += 1

            total += 1

        except:
            continue

accuracy = correct / total

print(f"System End-to-End Accuracy: {accuracy * 100:.2f}%")