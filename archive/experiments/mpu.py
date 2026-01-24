import socket

HOST = "0.0.0.0"
PORT = 5000

print("===================================")
print(" SignSpeak Smart Glove – Data View ")
print("===================================")
print("Waiting for ESP32 connection...\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

conn, addr = server.accept()
print(f"ESP32 connected from {addr}\n")

buffer = ""

try:
    while True:
        data = conn.recv(1024).decode(errors="ignore")
        if not data:
            break

        buffer += data

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()

            if not line:
                continue

            parts = line.split(",")

            # Expect: f1,f2,f3,ax,ay,az,gx,gy,gz (9 values)
            if len(parts) != 9:
                continue

            try:
                f1, f2, f3 = map(int, parts[:3])
                ax, ay, az, gx, gy, gz = map(float, parts[3:])

                print(
                    f"FLEX: {f1:4d} {f2:4d} {f3:4d}  ||  "
                    f"ACC: {ax:+.2f} {ay:+.2f} {az:+.2f}  ||  "
                    f"GYRO: {gx:+.0f} {gy:+.0f} {gz:+.0f}"
                )

            except ValueError:
                continue

except KeyboardInterrupt:
    print("\nStopped by user")

finally:
    conn.close()
    server.close()
