import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix

# CONFIG
MODEL_PATH = "models/efficientnet/skin_classifier.keras"
TEST_DIR = "training/dataset/cnn_dataset/test"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# LOAD MODEL
print("Loading trained CNN model...")
model = load_model(MODEL_PATH)
print("Model loaded successfully")

# LOAD TEST DATA
print("Loading test dataset...")

datagen = ImageDataGenerator(rescale=1./255)

test_generator = datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

class_names = list(test_generator.class_indices.keys())
print("Classes:", class_names)

# PREDICTION
print("\n🔍 Running inference on test data...")

predictions = model.predict(test_generator)
y_pred = np.argmax(predictions, axis=1)
y_true = test_generator.classes

# METRICS
print("\n📊 Classification Report:\n")

report = classification_report(y_true, y_pred, target_names=class_names)
print(report)

# SAVE REPORT
with open("classification_report.txt", "w") as f:
    f.write(report)

# CONFUSION MATRIX
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()

plt.savefig("confusion_matrix.png")
plt.show()

# ACCURACY
accuracy = np.sum(y_pred == y_true) / len(y_true)

print(f"\nFinal Test Accuracy: {accuracy * 100:.2f}%")

# PER-CLASS ACCURACY
print("\n📊 Per-class Accuracy:")

for i, class_name in enumerate(class_names):
    idx = np.where(y_true == i)[0]
    class_acc = np.mean(y_pred[idx] == y_true[idx])
    print(f"{class_name}: {class_acc * 100:.2f}%")