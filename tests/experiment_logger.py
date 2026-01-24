import socket
import csv
import time
import os

# ================= CONFIG =================
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
OUTPUT_FILE = "sensor_experiment_data.csv"

def parse_data(line):
    """
    Parses: "FLEX:f1,f2,f3,f4 | ACC:ax,ay,az | GYR:gx,gy,gz"
    """
    try:
        parts = line.split('|')
        
        # Parse FLEX
        flex_str = parts[0].split(':')[1]
        flex_vals = [float(x) for x in flex_str.split(',')]
        
        # Parse ACC
        acc_str = parts[1].split(':')[1]
        acc_vals = [float(x) for x in acc_str.split(',')]
        
        # Parse GYR
        gyr_str = parts[2].split(':')[1]
        gyr_vals = [float(x) for x in gyr_str.split(',')]
        
        return flex_vals, acc_vals, gyr_vals
    except Exception:
        return None, None, None

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind((UDP_IP, UDP_PORT))
    except OSError:
        print(f"❌ Error: Port {UDP_PORT} is busy. Stop the backend first!")
        return

    print(f"✅ LISTENING ON PORT {UDP_PORT}")
    print(f"📄 Logging data to: {OUTPUT_FILE}")
    print("Pre-Experiment: Checking headers...")
    
    # Write Header
    file_exists = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            headers = ["Timestamp", "Flex1", "Flex2", "Flex3", "Flex4", "AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ"]
            writer.writerow(headers)

    print("\n--- STARTING CAPTURE (Press Ctrl+C to stop) ---\n")

    try:
        while True:
            data, addr = sock.recvfrom(2048)
            message = data.decode("utf-8", errors="ignore").strip()

            if "FLEX:" in message:
                flex, acc, gyr = parse_data(message)
                
                if flex:
                    timestamp = time.strftime("%H:%M:%S")
                    
                    # Print to Screen
                    print(f"[{timestamp}] FLEX: {[f'{x:.3f}' for x in flex]} | ACC: {[f'{x:.3f}' for x in acc]} | GYR: {[f'{x:.3f}' for x in gyr]}")
                    
                    # Save to CSV
                    with open(OUTPUT_FILE, 'a', newline='') as f:
                        writer = csv.writer(f)
                        row = [timestamp] + flex + acc + gyr
                        writer.writerow(row)

    except KeyboardInterrupt:
        print("\n🛑 Experiment Stopped.")
        print(f"Data saved to {OUTPUT_FILE}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
