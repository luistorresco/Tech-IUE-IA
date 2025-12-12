import tensorflow as tf
import numpy as np
import cv2
import os

class SoilClassifier:
    def __init__(self, model_path="model_data/best_model.h5", classes_path="model_data/classes.txt"):
        self.model_path = model_path
        self.classes_path = classes_path
        self.model = None
        self.class_names = []
        self.load_artifacts()

    def load_artifacts(self):
        if os.path.exists(self.classes_path):
            with open(self.classes_path, "r") as f:
                self.class_names = [line.strip() for line in f.readlines()]
        else:
            print(f"Warning: Classes file not found at {self.classes_path}")

        if os.path.exists(self.model_path):
            try:
                self.model = tf.keras.models.load_model(self.model_path)
                print("Model loaded successfully.")
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print(f"Warning: Model file not found at {self.model_path}. Please run train.py first.")

    def predict(self, image_bytes):
        if self.model is None:
            raise Exception("Model is not loaded. Please train the model first.")

        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Preprocess
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)

        # Predict
        prediction = self.model.predict(img)
        class_idx = np.argmax(prediction[0])
        confidence = float(np.max(prediction[0]))
        
        predicted_class = self.class_names[class_idx] if self.class_names else str(class_idx)

        return predicted_class, confidence
