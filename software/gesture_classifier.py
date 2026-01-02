"""
SignSpeak - Gesture Classifier Module
Handles real-time gesture recognition from sensor data
"""

import numpy as np
import joblib
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GestureClassifier:
    """Real-time gesture classifier using Random Forest model"""
    
    def __init__(self, model_path=None, encoder_path=None):
        """
        Initialize gesture classifier
        
        Args:
            model_path: Path to trained model (default: ml/models/gesture_model.pkl)
            encoder_path: Path to label encoder (default: ml/models/label_encoder.pkl)
        """
        if model_path is None:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "ml", "models", "gesture_model.pkl"
            )
        if encoder_path is None:
            encoder_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "ml", "models", "label_encoder.pkl"
            )
        
        try:
            self.model = joblib.load(model_path)
            self.label_encoder = joblib.load(encoder_path)
            self.gestures = self.label_encoder.classes_
            print(f"✅ Gesture classifier loaded. Supported gestures: {list(self.gestures)}")
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Model files not found: {e}\n"
                "Please train the model first using ml/training/train_model.py"
            )
    
    def extract_features(self, window):
        """
        Extract mean and std features from sensor window
        
        Args:
            window: List of sensor readings (list of 11 values per frame)
            
        Returns:
            Feature vector (numpy array)
        """
        window_np = np.array(window)
        
        # Calculate mean and std for each sensor
        means = np.mean(window_np, axis=0)
        stds = np.std(window_np, axis=0)
        
        # Combine into feature vector
        features = []
        for m, s in zip(means, stds):
            features.append(m)
            features.append(s)
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, window):
        """
        Predict gesture from sensor window
        
        Args:
            window: List of sensor readings (list of 11 values per frame)
            
        Returns:
            Predicted gesture label (string)
        """
        features = self.extract_features(window)
        prediction = self.model.predict(features)
        gesture = self.label_encoder.inverse_transform(prediction)[0]
        return gesture
    
    def predict_with_confidence(self, window):
        """
        Predict gesture with confidence score
        
        Args:
            window: List of sensor readings
            
        Returns:
            Tuple of (gesture_label, confidence_score)
        """
        features = self.extract_features(window)
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = probabilities[prediction]
        gesture = self.label_encoder.inverse_transform([prediction])[0]
        return gesture, confidence

