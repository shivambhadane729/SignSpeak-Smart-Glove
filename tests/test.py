import serial
import time
import statistics

# ================= USER CONFIG =================
SERIAL_PORT = "COM10"      # CHANGE to your ESP32 COM port
BAUD_RATE = 115200

# Expected safe ranges (based on your calibration)
FLEX_RANGE = (0.0, 1.0)
ACC_RANGE  = (-1.5, 1.5)     # normalized g
GYR_RANGE  = (-0.2, 0.2)     # normalized gyro

WINDOW = 20   # frames for noise estimation

# ================= STORAGE =================
flex_history = [[] for _ in range(4)]
acc_history  = [[] for _ in range(3)]
gyr_history  = [[] for _ in range(3)]

# ================= HELPERS =================
def in_range(val, low, high):
    return low <= val <= high

def parse_line(line):
    """
    Parses:
    FLEX:a,b,c,d | ACC:x,y,z | GYR:p,q,r
    """
    try:
        parts = [p.strip() for p in line.split("|")]

        flex = list(map(float, parts[0].replace("FLEX:", "").split(",")))
        acc  = list(map(float, parts[1].replace("ACC:", "").split(",")))
        gyr  = list(map(float, parts[2].replace("GYR:", "").split(",")))

        if len(flex) != 4 or len(acc) != 3 or len(gyr) != 3:
            return None

        return flex, acc, gyr
    except Exception:
        return None

def update_history(hist, values):
    for i, v in enumerate(values):
        hist[i].append(v)
        if len(hist[i]) > WINDOW:
            hist[i].pop(0)

def noise_level(hist):
    if len(hist[0]) < WINDOW:
        return None
    return [round(statistics.pstdev(h), 4) for h in hist]

# ================= MAIN =================
def main():
    print("Connecting to ESP32...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)

    print("CONNECTED")
    print("Reading glove sensor stream...\n")

    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line or not line.startswith("FLEX"):
                continue

            parsed = parse_line(line)
            if not parsed:
                continue

            flex, acc, gyr = parsed

            update_history(flex_history, flex)
            update_history(acc_history, acc)
            update_history(gyr_history, gyr)

            flex_ok = all(in_range(v, *FLEX_RANGE) for v in flex)
            acc_ok  = all(in_range(v, *ACC_RANGE)  for v in acc)
            gyr_ok  = all(in_range(v, *GYR_RANGE)  for v in gyr)

            print(f"FLEX {flex} {'OK' if flex_ok else 'BAD'}")
            print(f"ACC  {acc} {'OK' if acc_ok else 'BAD'}")
            print(f"GYR  {gyr} {'OK' if gyr_ok else 'BAD'}")

            flex_noise = noise_level(flex_history)
            gyr_noise  = noise_level(gyr_history)

            if flex_noise:
                print("Flex noise (σ):", flex_noise)
            if gyr_noise:
                print("Gyro noise (σ):", gyr_noise)

            if not (flex_ok and acc_ok and gyr_ok):
                print("⚠ WARNING: VALUE OUT OF EXPECTED RANGE")

            print("-" * 60)

        except KeyboardInterrupt:
            print("\nStopping test.")
            break

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
