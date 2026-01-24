import sys
import os
import time
import socket

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gesture_rules import engine, FingerState, PalmOrientation

# ================= CONFIG =================
UDP_IP = "0.0.0.0"
UDP_PORT = 5005

def parse_packet(packet):
    try:
        parts = [p.strip() for p in packet.split("|")]
        flex = list(map(float, parts[0].replace("FLEX:", "").split(",")))
        acc  = list(map(float, parts[1].replace("ACC:", "").split(",")))
        gyr  = list(map(float, parts[2].replace("GYR:", "").split(",")))
        return flex, acc, gyr
    except:
        return None

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((UDP_IP, UDP_PORT))
    except OSError as e:
        print(f"Error: {e}. Is the backend or another script running?")
        return

    print("\n" + "="*60)
    print("🛠️  GESTURE CALIBRATION TOOL")
    print("Showing real-time states for each sensor.")
    print("Use this to verify your hand positions for the rules.")
    print("="*60 + "\n")
    
    # Header
    print(f"{'TIME':<10} | {'F1':<10} | {'F2':<10} | {'F3':<10} | {'F4':<10} | {'PALM':<12} | {'WORD'}")
    print("-" * 85)

    try:
        while True:
            data, addr = sock.recvfrom(2048)
            packet = data.decode("utf-8", errors="ignore").strip()
            
            parsed = parse_packet(packet)
            if not parsed:
                continue

            flex, acc, gyr = parsed
            
            # Get discrete states from engine
            f_states = [engine.get_finger_state(v) for v in flex]
            palm = engine.get_palm_orientation(*acc)
            word = engine.process_frame(flex, acc, gyr) or "---"
            
            # Print row (throttle to avoid flooding)
            # We'll use a simple print and only update if something changes or every 200ms
            t_str = time.strftime('%H:%M:%S')
            row = f"{t_str:<10} | {f_states[0]:<10} | {f_states[1]:<10} | {f_states[2]:<10} | {f_states[3]:<10} | {palm:<12} | {word}"
            
            # Use carriage return to stay on one line for "live" feel
            sys.stdout.write("\r" + row)
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\n🛑 Calibration stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
