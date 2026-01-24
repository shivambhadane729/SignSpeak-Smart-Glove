import socket
import time
from collections import deque

# ===================== SERVER CONFIG =====================
HOST = "0.0.0.0"
PORT = 5000

# ===================== THRESHOLDS (TUNED FOR YOUR DATA) =====================
IDLE_GYRO_THRESH = 10          # deg/s
MOTION_GYRO_THRESH = 40        # deg/s
STRONG_GYRO_THRESH = 80        # deg/s

IDLE_TIME_REQUIRED = 1.2       # seconds
GESTURE_WINDOW = 0.8           # seconds

SAMPLE_RATE = 20               # Hz
WINDOW_SIZE = int(GESTURE_WINDOW * SAMPLE_RATE)

# ===================== STATE VARIABLES =====================
gyro_window_x = deque(maxlen=WINDOW_SIZE)
gyro_window_y = deque(maxlen=WINDOW_SIZE)
gyro_window_z = deque(maxlen=WINDOW_SIZE)

last_motion_time = time.time()
last_detected_gesture = None

# ===================== SOCKET SETUP =====================
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("🟢 Waiting for ESP32...")
conn, addr = server.accept()
print(f"✅ Connected from {addr}")

buffer = ""

# ===================== HELPER FUNCTIONS =====================
def is_idle(gx, gy, gz):
    return (
        abs(gx) < IDLE_GYRO_THRESH and
        abs(gy) < IDLE_GYRO_THRESH and
        abs(gz) < IDLE_GYRO_THRESH
    )

def detect_hello(gy_values):
    peaks = sum(1 for v in gy_values if abs(v) > STRONG_GYRO_THRESH)
    return peaks >= 3

def detect_yes(gx_values):
    peaks = sum(1 for v in gx_values if abs(v) > STRONG_GYRO_THRESH)
    return peaks >= 2

def detect_no(gz_values):
    peaks = sum(1 for v in gz_values if abs(v) > STRONG_GYRO_THRESH)
    return peaks >= 2

# ===================== MAIN LOOP =====================
while True:
    data = conn.recv(1024).decode()
    buffer += data

    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        parts = line.strip().split(",")

        if len(parts) != 6:
            continue

        try:
            ax, ay, az, gx, gy, gz = map(float, parts)
        except ValueError:
            continue

        # Store gyro values
        gyro_window_x.append(gx)
        gyro_window_y.append(gy)
        gyro_window_z.append(gz)

        now = time.time()

        # ===================== IDLE / STOP =====================
        if is_idle(gx, gy, gz):
            if now - last_motion_time > IDLE_TIME_REQUIRED:
                if last_detected_gesture != "STOP":
                    print("🛑 GESTURE: STOP")
                    last_detected_gesture = "STOP"
            continue
        else:
            last_motion_time = now

        # ===================== GESTURE DETECTION =====================
        if len(gyro_window_y) == WINDOW_SIZE:
            if detect_hello(gyro_window_y):
                print("👋 GESTURE: HELLO")
                last_detected_gesture = "HELLO"
                gyro_window_x.clear()
                gyro_window_y.clear()
                gyro_window_z.clear()
                continue

            if detect_yes(gyro_window_x):
                print("👍 GESTURE: YES")
                last_detected_gesture = "YES"
                gyro_window_x.clear()
                gyro_window_y.clear()
                gyro_window_z.clear()
                continue

            if detect_no(gyro_window_z):
                print("❌ GESTURE: NO")
                last_detected_gesture = "NO"
                gyro_window_x.clear()
                gyro_window_y.clear()
                gyro_window_z.clear()
                continue
