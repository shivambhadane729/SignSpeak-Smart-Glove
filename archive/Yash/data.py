import serial
import json
import numpy as np
import pyttsx3
import time
import os

# --- 1. CONFIGURATION ---
PORT = 'COM9'
BAUD = 115200
FILE_NAME = "gesture_signatures.json"

SENTENCE_SEQUENCE = ["Hello", "I", "AM", "YASH", "We", "TEAM", "Fsociety"]

# --- 2. SPEECH MAP ---
SPEECH_MAP = {
    "Hello": "Hello",
    "I": "I",
    "AM": "am",
    "YASH": "Yash",
    "We": "We",
    "TEAM": "Team",
    "Fsociety": "F, society"
}

# --- 3. SPEECH FUNCTION ---
def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 145)
        print(f"🎤 Audio Output: {text}")
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"🔊 Speech Error: {e}")

# --- 4. LOAD SIGNATURES ---
if not os.path.exists(FILE_NAME):
    print("❌ Error: gesture_signatures.json not found")
    exit()

with open(FILE_NAME, "r") as f:
    signatures = json.load(f)

print(f"✅ Signatures loaded for: {', '.join(SENTENCE_SEQUENCE)}")

# --- 5. SERIAL CONNECT (ROBUST) ---
def connect_serial():
    while True:
        try:
            s = serial.Serial(PORT, BAUD, timeout=0.2)
            s.reset_input_buffer()
            print("🔌 Serial connected")
            return s
        except:
            print("⏳ Waiting for serial device...")
            time.sleep(1)

ser = connect_serial()

print("\n" + "=" * 45)
print("🚀 LIVE MODE | STABLE SERIAL | SAFE MATCHING")
print("=" * 45)

# --- 6. LIVE SEQUENTIAL MODE ---
current_index = 0
stability_counter = 0
REQUIRED_STABILITY = 10

while current_index < len(SENTENCE_SEQUENCE):
    gesture_id = SENTENCE_SEQUENCE[current_index]
    print(f"\n👉 WAITING FOR GESTURE: {gesture_id}")
    ser.reset_input_buffer()

    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()

            # Ignore empty lines or heartbeat
            if not line or line == "#":
                continue

            # Expect CSV of 10 values
            parts = line.split(",")
            if len(parts) != 10:
                continue

            vals = np.array([float(x) for x in parts])
            sig = signatures[gesture_id]

            mean = np.array(sig["mean"])
            std = np.array(sig["std"])

            # Avoid division-by-zero
            std[std == 0] = 1e-6

            error = np.mean(np.abs(vals - mean) / std)
            confidence = max(0, 100 - (error * 20))

            if confidence >= 70:
                stability_counter += 1
                print(
                    f"\rMatch: {confidence:.1f}% | Stability: {stability_counter}/{REQUIRED_STABILITY}",
                    end=""
                )

                if stability_counter >= REQUIRED_STABILITY:
                    print(f"\n✅ CONFIRMED: {gesture_id}")

                    speak_text(SPEECH_MAP.get(gesture_id, gesture_id))

                    current_index += 1
                    stability_counter = 0

                    if current_index < len(SENTENCE_SEQUENCE):
                        print("⏳ Reset hand to Neutral (Fist)...")
                        time.sleep(1.5)
                        ser.reset_input_buffer()

                    break
            else:
                stability_counter = 0

        except serial.SerialException as e:
            print(f"\n⚠ Serial error: {e}")
            try:
                ser.close()
            except:
                pass
            ser = connect_serial()
            break

        except Exception:
            # Ignore malformed frames safely
            continue

print("\n🏁 FINAL SEQUENCE COMPLETE")
time.sleep(1)
