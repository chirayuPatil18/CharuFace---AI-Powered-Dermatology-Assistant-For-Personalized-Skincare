from ultralytics import YOLO

# CONFIG
MODEL_PATH = "models/yolo/best.pt"  
DATA_PATH = "yolo_dataset/data.yaml"             

# LOAD MODEL
print("Loading YOLO model...")
model = YOLO(MODEL_PATH)

# EVALUATION
print("Running YOLO validation...")

metrics = model.val(data=DATA_PATH, split="test")

# PRINT RESULTS
print("\nYOLO Evaluation Results:\n")

print(f"mAP@0.5: {metrics.box.map50:.4f}")
print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")
print(f"Precision: {metrics.box.mp:.4f}")
print(f"Recall: {metrics.box.mr:.4f}")