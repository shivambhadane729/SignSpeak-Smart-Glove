import serial
import numpy as np
import joblib
import time

# ---------------- SETTINGS ----------------
PORT = "COM10"          # Change if needed
BAUD_RATE = 115200
WINDOW_SIZE = 20       # Same as training
# ------------------------------------------

# Load trained model and label encoder
model = joblib.load("gesture_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

print("✅ Model & label encoder loaded")
print(f"🖐️ Gestures: {label_encoder.classes_}\n")

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)

print("📡 Listening for gestures...")
print("👉 Perform gesture now\n")

# Flush junk lines
for _ in range(10):
    ser.readline()

while True:
    try:
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

        window_np = np.array(window)

        # Feature extraction (mean + std)
        means = np.mean(window_np, axis=0)
        stds  = np.std(window_np, axis=0)

        features = []
        for m, s in zip(means, stds):
            features.append(m)
            features.append(s)

        features = np.array(features).reshape(1, -1)

        # Predict
        prediction = model.predict(features)
        gesture = label_encoder.inverse_transform(prediction)[0]

        print(f"🧠 Predicted Gesture: {gesture}")

    except KeyboardInterrupt:
        print("\n🛑 Live testing stopped")
        ser.close()
        break
