import serial
import time
import pandas as pd

# ===== CONFIG =====
PORT = "COM10"        # 🔴 change to your ESP32 COM port
BAUD = 115200
GESTURE_NAME = "IDLE"
SAMPLES_PER_GESTURE = 50   # 1 second @ 50Hz
TOTAL_GESTURES = 100

# ==================

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

print("✅ Connected to ESP32")
print(f"Collecting {TOTAL_GESTURES} '{GESTURE_NAME}' gestures")
print("Press ENTER to START each gesture\n")

data = []
gesture_id = 0

while gesture_id < TOTAL_GESTURES:
    input(f"[Gesture {gesture_id+1}] Press ENTER and perform HELLO gesture...")

    start_time = time.time()
    samples_collected = 0

    while samples_collected < SAMPLES_PER_GESTURE:
        line = ser.readline().decode("utf-8").strip()
        if not line:
            continue

        try:
            ax, ay, az, gx, gy, gz = map(int, line.split(","))

            data.append([
                gesture_id,
                GESTURE_NAME,
                start_time,
                None,          # end_time (fill later)
                ax, ay, az,
                gx, gy, gz
            ])

            samples_collected += 1

        except ValueError:
            continue

    end_time = time.time()

    # Fill end_time for this gesture
    for i in range(len(data)-samples_collected, len(data)):
        data[i][3] = end_time

    print(f"✅ Gesture {gesture_id+1} recorded\n")
    gesture_id += 1

# Save to CSV
columns = [
    "gesture_id",
    "label",
    "start_time",
    "end_time",
    "ax", "ay", "az",
    "gx", "gy", "gz"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("thankyou.csv", index=False)

print("🎉 Data collection complete!")
print("Saved as thankyou.csv")
