import serial
import csv
import time

# =========================
# CONFIG
# =========================
PORT = 'COM10'
BAUD = 115200
FILE_NAME = 'gesture_data.csv'

SAMPLES_PER_WINDOW = 40
SENSORS_PER_SAMPLE = 11   # MUST match ESP32 output
SAMPLES_PER_GESTURE = 15

TOTAL_FEATURES = SAMPLES_PER_WINDOW * SENSORS_PER_SAMPLE

# =========================
# RECORD FUNCTION
# =========================
def record_gesture(label, ser):
    print(f"\nPrepare for: [{label}]")
    time.sleep(2)
    print(">>> START MOTION NOW! <<<")

    window_data = []

    while len(window_data) < TOTAL_FEATURES:
        line = ser.readline().decode('utf-8', errors='ignore').strip()

        # Skip empty or noisy lines
        if not line or ',' not in line:
            continue

        parts = line.split(',')

        # Validate sensor count
        if len(parts) != SENSORS_PER_SAMPLE:
            continue

        try:
            values = [float(x) for x in parts]
            window_data.extend(values)
        except ValueError:
            continue

    # Append label
    window_data.append(label)
    return window_data

# =========================
# MAIN
# =========================
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # allow ESP32 reset

    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)

        while True:
            gesture = input("\nEnter gesture name (or 'q' to quit): ").upper()
            if gesture == 'Q':
                break

            for i in range(SAMPLES_PER_GESTURE):
                print(f"Recording {gesture} - Sample {i+1}/{SAMPLES_PER_GESTURE}")
                row = record_gesture(gesture, ser)
                writer.writerow(row)
                print("✔ Captured")

except Exception as e:
    print(f"❌ Error: {e}")
