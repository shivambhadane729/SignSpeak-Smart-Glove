import sys
import os
import time
import socket
import numpy as np

# ================= CONFIG =================
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
SAMPLES_TO_CAPTURE = 50

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
    if len(sys.argv) < 2:
        gesture_name = input("Enter gesture name (e.g., Hello, Yash): ").strip()
        if not gesture_name:
            print("Gesture name is required.")
            return
    else:
        gesture_name = sys.argv[1]
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((UDP_IP, UDP_PORT))
    except OSError as e:
        print(f"Error: {e}. Is the backend running?")
        return

    print(f"\n🚀 READY TO CAPTURE SIGNATURE FOR: {gesture_name}")
    print("1. Perform the gesture and hold it steady.")
    print("2. Press ENTER to start a 2-second capture...")
    input()
    
    print(f"Capturing {SAMPLES_TO_CAPTURE} samples...")
    
    flex_data = []
    acc_data = []
    
    captured = 0
    while captured < SAMPLES_TO_CAPTURE:
        data, addr = sock.recvfrom(2048)
        packet = data.decode("utf-8", errors="ignore").strip()
        parsed = parse_packet(packet)
        
        if parsed:
            flex, acc, gyr = parsed
            flex_data.append(flex)
            acc_data.append(acc)
            captured += 1
            if captured % 10 == 0:
                print(f"[{captured}/{SAMPLES_TO_CAPTURE}]...")

    # Calculate statistics
    flex_np = np.array(flex_data)
    acc_np = np.array(acc_data)
    
    flex_means = np.mean(flex_np, axis=0)
    acc_means = np.mean(acc_np, axis=0)
    
    print("\n" + "="*50)
    print(f"📊 GESTURE SIGNATURE: {gesture_name}")
    print("="*50)
    print(f"F1 (Thumb):  {flex_means[0]:.4f}")
    print(f"F2 (Index):  {flex_means[1]:.4f}")
    print(f"F3 (Middle): {flex_means[2]:.4f}")
    print(f"F4 (Ring):   {flex_means[3]:.4f}")
    print(f"ACC (Z-axis):{acc_means[2]:.4f} (Palm Orientation)")
    print("="*50)
    print("\nPlease copy the values above and send them to me!")
    print("="*50 + "\n")

    sock.close()

if __name__ == "__main__":
    main()
