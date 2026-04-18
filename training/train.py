import numpy as np
import tensorflow as tf
from keras.applications import MobileNetV2
from keras.layers import Dense, GlobalAveragePooling2D, Dropout
from keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.losses import CategoricalCrossentropy

# CONFIG
DATA_DIR = "training/dataset/labeled_data"
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20
MODEL_PATH = "models/efficientnet/skin_classifier.keras"

# Efficient preprocessing
from keras.applications.mobilenet_v2 import preprocess_input

datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,
    rotation_range=10,
    zoom_range=0.1,
    horizontal_flip=True
)

train_gen = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_gen = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

print("Classes:", train_gen.class_indices)

# MODEL
base_model = MobileNetV2(
    include_top=False,
    weights="imagenet",
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)
x = Dropout(0.5)(x)
outputs = Dense(train_gen.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=outputs)

# COMPILE 
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=3e-4),
    loss=CategoricalCrossentropy(label_smoothing=0.1),  # helps noisy data
    metrics=["accuracy"]
)

callbacks = [
    EarlyStopping(patience=12, restore_best_weights=True),
    ModelCheckpoint(MODEL_PATH, save_best_only=True)
]

print("Training started...")

model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=callbacks
)

# ---------------- SAVE ----------------
model.save(MODEL_PATH)

print("Model trained and saved!")