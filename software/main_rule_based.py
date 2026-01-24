import sys
import os
import time
import socket

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gesture_rules import engine

# ================= CONFIG =================
UDP_IP = "0.0.0.0"
UDP_PORT = 5005

def parse_packet(packet):
    """
    Parses the ESP32 packet format:
    FLEX:f1,f2,f3,f4 | ACC:ax,ay,az | GYR:gx,gy,gz
    """
    try:
        parts = [p.strip() for p in packet.split("|")]
        flex = list(map(float, parts[0].replace("FLEX:", "").split(",")))
        acc  = list(map(float, parts[1].replace("ACC:", "").split(",")))
        gyr  = list(map(float, parts[2].replace("GYR:", "").split(",")))
        return flex, acc, gyr
    except Exception as e:
        return None

def main():
    # Setup UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((UDP_IP, UDP_PORT))
    except OSError as e:
        print(f"Error binding to port {UDP_PORT}: {e}")
        print("Make sure no other instance is running (like the old backend).")
        return

    print("\n" + "="*40)
    print("🚀 SIGN SPEAK - RULE-BASED ENGINE")
    print("Listening for gestures on port 5005...")
    print("Gestures: Hello, I, Yash, We, Team Fsociety")
    print("="*40 + "\n")

    last_gesture = None
    last_detect_time = 0
    COOLDOWN = 1.5 # Seconds between different detections

    try:
        while True:
            data, addr = sock.recvfrom(2048)
            packet = data.decode("utf-8", errors="ignore").strip()
            
            parsed = parse_packet(packet)
            if not parsed:
                continue

            flex, acc, gyr = parsed
            
            # Use the rule engine
            gesture = engine.process_frame(flex, acc, gyr)

            if gesture:
                current_time = time.time()
                # Detection logic with cooldown and change detection
                if gesture != last_gesture or (current_time - last_detect_time > COOLDOWN):
                    print(f"[{time.strftime('%H:%M:%S')}] Detected: {gesture}")
                    last_gesture = gesture
                    last_detect_time = current_time
                    
            elif last_gesture:
                # If gesture is lost (hand moves or opens), we can reset or just wait
                # For now, let's keep it simple: no gesture means no detection output
                pass

    except KeyboardInterrupt:
        print("\n🛑 Shutting down Gesture Engine...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
