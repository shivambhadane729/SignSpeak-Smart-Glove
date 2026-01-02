import serial
import csv
import time

# --- CONFIGURATION ---
PORT = 'COM10'  # Change to your ESP32 port
BAUD = 115200
FILE_NAME = 'gesture_data.csv'
SAMPLES_PER_WINDOW = 40  # ~2 seconds of motion at 20Hz

def record_gesture(label, ser):
    print(f"\nPrepare for: [{label}]")
    time.sleep(2)
    print(">>> START MOTION NOW! <<<")
    
    window_data = []
    for _ in range(SAMPLES_PER_WINDOW):
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                # Expecting: flex1,flex2,flex3,flex4,flex5,ax,ay,az,gx,gy,gz
                vals = [float(x) for x in line.split(',')]
                window_data.extend(vals) # Flattening the window
            except:
                continue
    
    window_data.append(label)
    return window_data

try:
    ser = serial.Serial(PORT, BAUD)
    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        while True:
            target = input("Enter gesture name to record (or 'q' to quit): ").upper()
            if target == 'Q': break
            
            for i in range(15): # Record 15 samples per gesture
                print(f"Recording {target} - Sample {i+1}/15")
                row = record_gesture(target, ser)
                writer.writerow(row)
                print("Captured!")
except Exception as e:
    print(f"Error: {e}")