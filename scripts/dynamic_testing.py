import serial
import pickle
import numpy as np
import pyttsx3
import time

# ======================
# CONFIG
# ======================
PORT = 'COM10'
BAUD = 115200

BUFFER_SIZE = 40
SENSORS_PER_SAMPLE = 11

CONFIDENCE_THRESHOLD = 0.6
COOLDOWN_SECONDS = 0.5

PREDICT_EVERY_N_FRAMES = 5     # 🔥 KEY OPTIMIZATION
MOVEMENT_THRESHOLD = 3.0       # ignore idle hand

# ======================
# INIT SERIAL
# ======================
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

# ======================
# LOAD MODEL & ENCODER
# ======================
with open('glove_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# ======================
# TTS SETUP
# ======================
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

engine.say("Glove system ready")
engine.runAndWait()

# ======================
# STATE
# ======================
data_buffer = []
frame_count = 0

last_spoken_time = 0
last_prediction = None

print("🧤 Glove Active. Start Signing...")

# ======================
# MAIN LOOP
# ======================
while True:
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line or ',' not in line:
            continue

        parts = line.split(',')
        if len(parts) != SENSORS_PER_SAMPLE:
            continue

        current_vals = np.array([float(x) for x in parts])
        data_buffer.append(current_vals)

        if len(data_buffer) > BUFFER_SIZE:
            data_buffer.pop(0)

        if len(data_buffer) < BUFFER_SIZE:
            continue

        # 🔥 SKIP FRAMES
        frame_count += 1
        if frame_count % PREDICT_EVERY_N_FRAMES != 0:
            continue

        # 🔥 MOVEMENT CHECK (skip idle hand)
        motion_energy = np.mean(np.abs(np.diff(data_buffer, axis=0)))
        if motion_energy < MOVEMENT_THRESHOLD:
            continue

        # 🔥 MODEL INFERENCE
        flattened = np.array(data_buffer).flatten().reshape(1, -1)

        pred_index = model.predict(flattened)[0]   # FAST
        probs = model.predict_proba(flattened)[0]  # SLOW (only now)

        confidence = probs[pred_index]
        prediction = label_encoder.inverse_transform([pred_index])[0]

        now = time.time()

        if (
            confidence >= CONFIDENCE_THRESHOLD and
            now - last_spoken_time >= COOLDOWN_SECONDS and
            prediction != last_prediction
        ):
            print(f"Detected: {prediction} ({confidence*100:.1f}%)")
            engine.say(prediction)
            engine.runAndWait()

            last_spoken_time = now
            last_prediction = prediction

            data_buffer = data_buffer[-10:]   # keep history

    except Exception:
        continue
