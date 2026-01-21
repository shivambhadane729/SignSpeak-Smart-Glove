import serial
import json
import time
import keyboard
import os

PORT = "COM5"
BAUD = 115200
GESTURE = "hello"

os.makedirs("data", exist_ok=True)

ser = serial.Serial(PORT, BAUD)
time.sleep(2)

dataset = {
    "label": GESTURE,
    "sampling_rate": 100,
    "gestures": []
}

recording = False
buffer = []

print("\nControls:")
print("  s → START gesture capture")
print("  e → END gesture capture")
print("  q → QUIT and save\n")

while True:
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        try:
            t, ax, ay, az, gx, gy, gz = map(float, line.split(","))
        except:
            continue

        if recording:
            buffer.append([t, ax, ay, az, gx, gy, gz])

    if keyboard.is_pressed("s") and not recording:
        print("🟢 Recording started")
        buffer = []
        recording = True
        time.sleep(0.3)

    if keyboard.is_pressed("e") and recording:
        recording = False
        if len(buffer) > 10:
            dataset["gestures"].append(buffer)
            print(f"✅ Gesture saved ({len(dataset['gestures'])})")
        else:
            print("❌ Gesture too short, discarded")
        buffer = []
        time.sleep(0.3)

    if keyboard.is_pressed("q"):
        print("💾 Saving and exiting")
        break

ser.close()

with open(f"data/{GESTURE}.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("Done.")
