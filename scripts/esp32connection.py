import socket

# ===================== CONFIG =====================
HOST = "0.0.0.0"   # Listen on all interfaces
PORT = 5000        # Must match ESP32 code

# ===================== SERVER SETUP =====================
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("🟢 Waiting for ESP32 connection...")
conn, addr = server.accept()
print(f"✅ Connected from {addr}")

buffer = ""

# ===================== MAIN LOOP =====================
while True:
    try:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            print("❌ Connection closed")
            break

        buffer += data

        # Process complete lines only
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()

            if not line:
                continue

            parts = line.split(",")

            # Validate IMU packet (6 values)
            if len(parts) != 6:
                continue

            try:
                ax, ay, az, gx, gy, gz = map(float, parts)
            except ValueError:
                continue

            # ===================== OUTPUT =====================
            print(f"AX:{ax:6.2f}  AY:{ay:6.2f}  AZ:{az:6.2f} | "
                  f"GX:{gx:7.2f}  GY:{gy:7.2f}  GZ:{gz:7.2f}")

            # ===================== PLACE FOR MAPPING =====================
            # Example:
            # if abs(gy) > 120:
            #     print("Gesture: HELLO")

    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        break

# ===================== CLEANUP =====================
conn.close()
server.close()
