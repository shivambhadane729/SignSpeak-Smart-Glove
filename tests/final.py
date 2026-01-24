import socket
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

GYRO_STATIC_THRESHOLD = 0.08

def parse_packet(packet):
    try:
        parts = [p.strip() for p in packet.split("|")]
        flex = list(map(float, parts[0].replace("FLEX:", "").split(",")))
        acc  = list(map(float, parts[1].replace("ACC:", "").split(",")))
        gyr  = list(map(float, parts[2].replace("GYR:", "").split(",")))
        return flex, acc, gyr
    except:
        return None

def is_static(gyr):
    return abs(gyr[0]) + abs(gyr[1]) + abs(gyr[2]) < GYRO_STATIC_THRESHOLD

def detect_word(flex, acc, gyr):
    if not is_static(gyr):
        return None

    f1, f2, f3, f4 = flex
    ax, ay, az = acc

    # HELLO
    if f2 < 0.05 and f3 < 0.05 and az > 0.6:
        return "HELLO"

    # I
    if f2 < 0.05 and f3 < 0.05 and az < 0.2:
        return "I"

    return None

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print("🧠 Word detection started (HELLO vs I)")
    print("Hold a static gesture...\n")

    last_word = None

    while True:
        data, _ = sock.recvfrom(2048)
        packet = data.decode("utf-8", errors="ignore").strip()

        parsed = parse_packet(packet)
        if not parsed:
            continue

        flex, acc, gyr = parsed
        word = detect_word(flex, acc, gyr)

        if word and word != last_word:
            print(f"[{time.strftime('%H:%M:%S')}] Detected → {word}")
            last_word = word

if __name__ == "__main__":
    main()
