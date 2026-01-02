"""
SignSpeak - Real-time Gesture Inference
Loads trained model and performs live gesture recognition from serial data
"""

import serial
import numpy as np
import joblib
import time
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------- SETTINGS ----------------
PORT = "COM10"          # Change if needed
BAUD_RATE = 115200
WINDOW_SIZE = 20       # Same as training
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "gesture_model.pkl")
ENCODER_PATH = os.path.join(os.path.dirname(__file__), "models", "label_encoder.pkl")
# ------------------------------------------

def load_model():
    """Load trained model and label encoder"""
    try:
        model = joblib.load(MODEL_PATH)
        label_encoder = joblib.load(ENCODER_PATH)
        print("✅ Model & label encoder loaded")
        print(f"🖐️ Gestures: {label_encoder.classes_}\n")
        return model, label_encoder
    except FileNotFoundError as e:
        print(f"❌ Error loading model: {e}")
        print("💡 Make sure to train the model first using ml/training/train_model.py")
        sys.exit(1)

def extract_features(window):
    """Extract mean and std features from sensor window"""
    window_np = np.array(window)
    
    # Feature extraction (mean + std)
    means = np.mean(window_np, axis=0)
    stds = np.std(window_np, axis=0)
    
    features = []
    for m, s in zip(means, stds):
        features.append(m)
        features.append(s)
    
    return np.array(features).reshape(1, -1)

def predict_gesture(model, label_encoder, features):
    """Predict gesture from features"""
    prediction = model.predict(features)
    gesture = label_encoder.inverse_transform(prediction)[0]
    return gesture

def main():
    """Main inference loop"""
    # Load model
    model, label_encoder = load_model()
    
    # Open serial port
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
    except Exception as e:
        print(f"❌ Could not open serial port {PORT}: {e}")
        sys.exit(1)
    
    print("📡 Listening for gestures...")
    print("👉 Perform gesture now\n")
    
    # Flush junk lines
    for _ in range(10):
        ser.readline()
    
    try:
        while True:
            window = []
            
            # Collect one motion window
            while len(window) < WINDOW_SIZE:
                line = ser.readline().decode("utf-8").strip()
                
                if not line or line.startswith("thumb"):
                    continue
                
                values = line.split(",")
                
                if len(values) != 11:
                    continue
                
                window.append([float(v) for v in values])
            
            # Extract features and predict
            features = extract_features(window)
            gesture = predict_gesture(model, label_encoder, features)
            
            print(f"🧠 Predicted Gesture: {gesture}")
            
    except KeyboardInterrupt:
        print("\n🛑 Live testing stopped")
        ser.close()

if __name__ == "__main__":
    main()

