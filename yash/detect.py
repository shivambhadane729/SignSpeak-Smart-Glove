import serial
import joblib
import pyttsx3
import time
import pandas as pd
import warnings
import sys

# Suppress warnings for clean output
warnings.filterwarnings("ignore", category=UserWarning)

# --- CONFIG ---
PORT = 'COM10' 
BAUD = 115200
MODEL_PATH = 'signspeak.pkl'
COLUMNS = ['f1', 'f2', 'f3', 'f4', 'ax', 'ay', 'az']

# 1. Initialize Audio
engine = pyttsx3.init()
engine.setProperty('rate', 160) # Natural speed

# 2. Load Model
try:
    model = joblib.load(MODEL_PATH)
    print("Step 1: AI Model Loaded.")
except:
    sys.exit("Error: Run train.py first to create the model file.")

# 3. Connect to ESP32
try:
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    time.sleep(2)
    print(f"Step 2: Connected to {PORT}. START SIGNING!")
except:
    sys.exit(f"Error: Could not connect to {PORT}.")

# --- LOGIC ---
last_spoken = ""
stability_counter = 0
current_guess = ""
STABILITY_THRESHOLD = 5 # Balanced speed (approx 150ms of hold time)

try:
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        
        if line and line.count(',') == 6:
            try:
                parts = line.split(',')
                features = [float(x) for x in parts[:7]]
                features_df = pd.DataFrame([features], columns=COLUMNS)
                
                prediction = model.predict(features_df)[0]
                
                # Accuracy/Stability check
                if prediction == current_guess:
                    stability_counter += 1
                else:
                    current_guess = prediction
                    stability_counter = 0
                
                # Output
                if stability_counter >= STABILITY_THRESHOLD:
                    if prediction != last_spoken:
                        print(f"MESSAGE: {prediction}")
                        engine.say(prediction)
                        engine.runAndWait()
                        
                        last_spoken = prediction
                        stability_counter = 0
                        time.sleep(0.3) # Time to switch gestures

            except Exception:
                continue

except KeyboardInterrupt:
    print("\nSystem stopped.")
finally:
    ser.close()