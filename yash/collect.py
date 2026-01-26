import serial
import csv
import time
import os

# --- CONFIGURATION ---
PORT = 'COM10'
BAUD = 115200
FILENAME = "training_data.csv"
RECORD_TIME = 25  # 25 seconds per word
GAP_TIME = 5      # 5 seconds to change gestures

# --- THE SEQUENCE ---
# "TEAM_FSOCIETY" is now one single label
sentence_words = ["HELLO", "I", "AM", "YASH", "WE", "ARE", "TEAM_FSOCIETY"]

def start_fresh_collection():
    # 1. Initialize Serial
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2) 
        print(f"--- Connected to {PORT} ---")
    except Exception as e:
        print(f"ERROR: Could not open {PORT}. Close Arduino Serial Monitor first!")
        return

    # 2. Delete old file to start from scratch
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
        print(f"Cleaned old data. Starting fresh.")

    # 3. Loop through words
    for word in sentence_words:
        print(f"\n\nNEXT WORD: {word}")
        for i in range(GAP_TIME, 0, -1):
            print(f"Get ready for '{word}'... Starting in {i}s", end='\r')
            time.sleep(1)
        
        print(f"\n>>> RECORDING: {word} (25 Seconds) <<<")
        start_time = time.time()
        samples_captured = 0
        
        with open(FILENAME, 'a', newline='') as f:
            writer = csv.writer(f)
            ser.reset_input_buffer() 
            
            while (time.time() - start_time) < RECORD_TIME:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line and "," in line:
                        parts = line.split(',')
                        if len(parts) == 7: # Expecting 4 flex + 3 accel
                            writer.writerow(parts + [word])
                            samples_captured += 1
                            
                            rem = int(RECORD_TIME - (time.time() - start_time))
                            print(f"  [SAVING] {word} | Time: {rem}s | Samples: {samples_captured}  ", end='\r')
                except Exception:
                    continue
        
        print(f"\n>>> SUCCESS: Finished '{word}'")
    
    ser.close()
    print("\n" + "="*40)
    print("ALL DONE! Your new CSV is ready.")
    print("="*40)

# --- EXECUTION ---
if __name__ == "__main__":
    print("--- SignSpeak Final Data Collector ---")
    print(f"Words: {' -> '.join(sentence_words)}")
    start_fresh_collection()