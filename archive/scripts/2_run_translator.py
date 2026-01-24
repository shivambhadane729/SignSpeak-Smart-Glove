import serial
import csv
import time

ser = serial.Serial('COM10', 115200) # Your ESP32 Port
LABEL = "HELLO"
SAMPLES_PER_GESTURE = 40  # 2 seconds at 20Hz
TOTAL_RECORDINGS = 20     # Record "Hello" 20 times

with open('dynamic_data.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    for i in range(TOTAL_RECORDINGS):
        print(f"Get ready to perform: {LABEL} ({i+1}/{TOTAL_RECORDINGS})")
        time.sleep(2)
        print("START MOTION NOW!")
        
        window = []
        for _ in range(SAMPLES_PER_GESTURE):
            line = ser.readline().decode('utf-8').strip()
            data = [float(x) for x in line.split(',')]
            window.extend(data) # This "flattens" the motion into one row
        
        window.append(LABEL) # Add the name at the end
        writer.writerow(window)
        print("Done. Rest for a second...")