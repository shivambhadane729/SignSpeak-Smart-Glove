import serial
import csv
import time
import os
import numpy as np

# ---------- USER SETTINGS ----------
PORT = "COM10"            # Change this
BAUD_RATE = 115200
WINDOW_SIZE = 20         # Frames per gesture (~1 sec at 20Hz)
SAMPLES_PER_GESTURE = 120
# -----------------------------------

label = input("Enter gesture label (e.g., HELLO, YES): ").strip().upper()
dataset_path = os.path.join(os.path.dirname(__file__), "..", "dataset")
os.makedirs(dataset_path, exist_ok=True)
filename = os.path.join(dataset_path, f"{label}_dynamic.csv")

file_exists = os.path.isfile(filename)

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
except:
    print("❌ Could not open serial port")
    exit()

print(f"\n📥 Collecting DYNAMIC gesture: {label}")
print("👉 Perform ONE full gesture motion when prompted\n")

with open(filename, "a", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        header = ["label"]
        sensors = [
            "thumb", "index", "middle", "ring", "pinky",
            "accX", "accY", "accZ",
            "gyroX", "gyroY", "gyroZ"
        ]
        for s in sensors:
            header.append(f"{s}_mean")
            header.append(f"{s}_std")
        writer.writerow(header)

    count = 0

    # Flush junk lines
    for _ in range(10):
        ser.readline()

    while count < SAMPLES_PER_GESTURE:
        print(f"\n🎬 Perform gesture #{count + 1}")
        window = []

        while len(window) < WINDOW_SIZE:
            line = ser.readline().decode("utf-8").strip()

            if not line or line.startswith("thumb"):
                continue

            values = line.split(",")

            if len(values) != 11:
                continue

            window.append([float(v) for v in values])

        window_np = np.array(window)

        means = np.mean(window_np, axis=0)
        stds  = np.std(window_np, axis=0)

        row = [label]
        for m, s in zip(means, stds):
            row.append(round(m, 2))
            row.append(round(s, 2))

        writer.writerow(row)
        count += 1

        print(f"✅ Saved sample {count}/{SAMPLES_PER_GESTURE}")

print("\n🎉 Dynamic gesture data collection completed!")
ser.close()
