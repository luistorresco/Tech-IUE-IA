import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from pathlib import Path
import cv2

# Configuration
DATA_PATH = Path("../archive (1)/Orignal-Dataset")
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20 # Reduced for demonstration, user can increase
MODEL_SAVE_PATH = "model_data/best_model.h5"

def load_data(data_path):
    images = []
    labels = []
    class_names = sorted([d.name for d in data_path.iterdir() if d.is_dir()])
    print(f"Classes found: {class_names}")

    for class_idx, class_name in enumerate(class_names):
        class_path = data_path / class_name
        image_files = list(class_path.glob('*.jpg')) + list(class_path.glob('*.png')) + list(class_path.glob('*.jpeg'))
        
        print(f"Loading {class_name}: {len(image_files)} images")
        for img_path in image_files:
            try:
                img = cv2.imread(str(img_path))
                if img is None: continue
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, IMG_SIZE)
                images.append(img)
                labels.append(class_idx)
            except Exception as e:
                pass
    
    return np.array(images), np.array(labels), class_names

def create_model(num_classes):
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    base_model.trainable = False # Start with frozen base

    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    predictions = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(inputs=base_model.input, outputs=predictions)
    return model

def main():
    if not DATA_PATH.exists():
        print(f"Error: Data path {DATA_PATH} not found.")
        return

    # Ensure output dir exists
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

    print("Loading data...")
    X, y, class_names = load_data(DATA_PATH)
    
    # Normalize
    X = X.astype('float32') / 255.0

    # Save class names for inference
    with open("model_data/classes.txt", "w") as f:
        f.write("\n".join(class_names))

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    print(f"Training on {len(X_train)} samples, Validating on {len(X_val)} samples.")

    model = create_model(len(class_names))
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True),
        ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True, monitor='val_accuracy')
    ]

    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks
    )

    print(f"Model saved to {MODEL_SAVE_PATH}")
    print("Training Complete.")

if __name__ == "__main__":
    main()
