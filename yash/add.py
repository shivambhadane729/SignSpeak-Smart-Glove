import serial
import csv
import time
import os
import sys

# --- CONFIGURATION ---
PORT = 'COM10'  
BAUD = 115200
FILENAME = "training_data.csv"
RECORD_TIME = 25  # 25 seconds per word
GAP_TIME = 5      # 5 seconds to switch gestures

# 1. Initialize Serial
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2) 
    print(f"--- Connected to {PORT} ---")
except Exception as e:
    print(f"ERROR: Could not open {PORT}. Make sure Arduino Serial Monitor is CLOSED!")
    sys.exit()

def capture_sequence(word_list):
    print(f"Adding data for {word_list} to: {FILENAME}")

    for word in word_list:
        # --- PREPARATION PHASE ---
        print(f"\n\nNEXT WORD: {word}")
        for i in range(GAP_TIME, 0, -1):
            print(f"Prepare hand for '{word}'... Starting in {i}s", end='\r')
            time.sleep(1)
        
        print(f"\n>>> RECORDING '{word}' NOW! (25 Seconds) <<<")
        start_time = time.time()
        count = 0
        
        # 2. Open in 'a' (Append) mode
        try:
            with open(FILENAME, 'a', newline='') as f:
                writer = csv.writer(f)
                ser.reset_input_buffer() 
                
                while (time.time() - start_time) < RECORD_TIME:
                    try:
                        line = ser.readline().decode('utf-8', errors='ignore').strip()
                        if line and "," in line:
                            parts = line.split(',')
                            # Expecting 7 values: 4 flex sensors + 3 accel axes
                            if len(parts) == 7:
                                writer.writerow(parts + [word])
                                count += 1
                                
                                # Progress update
                                elapsed = int(time.time() - start_time)
                                print(f"  [SAVING] {word} | Time Left: {RECORD_TIME - elapsed}s | Samples: {count}  ", end='\r')
                    except Exception:
                        continue
            
            print(f"\n>>> SUCCESS: Finished recording '{word}'")
            
        except PermissionError:
            print(f"\n❌ ERROR: Permission Denied. Close '{FILENAME}' in Excel/Notepad and try again!")
            return

# --- TARGET WORDS ---
target_words = ["AM", "ARE"]

print("--- SignSpeak Data Appender ---")
print(f"Sequence: {' -> '.join(target_words)}")

confirm = input("\nPress 's' to start the automatic 25s/word recording: ").lower().strip()

if confirm == 's':
    capture_sequence(target_words)
    print("\n" + "="*40)
    print("ALL DATA SAVED SUCCESSFULLY!")
    print(f"Your CSV now has updated data for 'AM' and 'ARE'.")
    print("="*40)
    print("Final Step: Run your 'train.py' script to update the model.")
else:
    print("Cancelled.")

ser.close()