import socket
import csv
import math
import os
import time

# ================= CONFIG =================
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
DATA_DIR = r"..\Mapping\Phase1" # Relative to 'tests/' folder

# ================= CLASSIFIER =================
class SimpleClassifier:
    def __init__(self):
        self.centroids = {} # { "LABEL": [f1, f2, f3, f4] }

    def load_training_data(self):
        print("Loading datasets...")
        if not os.path.exists(DATA_DIR):
             print(f"❌ Error: Data directory '{DATA_DIR}' not found!")
             return

        files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
        
        for file in files:
            label = file.replace("dataset_", "").replace(".csv", "")
            path = os.path.join(DATA_DIR, file)
            
            flex_sums = [0.0] * 4
            count = 0
            
            try:
                with open(path, 'r') as f:
                    reader = csv.reader(f)
                    next(reader) # Skip header
                    for row in reader:
                        # Row format: [timestamp, f1, f2, f3, f4, ...]
                        # Flex are indices 1, 2, 3, 4
                        f_vals = [float(row[1]), float(row[2]), float(row[3]), float(row[4])]
                        for i in range(4):
                            flex_sums[i] += f_vals[i]
                        count += 1
                
                if count > 0:
                    means = [s / count for s in flex_sums]
                    self.centroids[label] = means
                    print(f"   ✅ Trained '{label}' (Samples: {count}) -> Mean: {[round(x,3) for x in means]}")
            except Exception as e:
                print(f"   ⚠️ Could not load {file}: {e}")

    def predict(self, current_flex):
        best_label = "UNKNOWN"
        min_dist = 9999.0
        
        for label, centroid in self.centroids.items():
            # Euclidean Distance
            dist = math.sqrt(sum((current_flex[i] - centroid[i])**2 for i in range(4)))
            if dist < min_dist:
                min_dist = dist
                best_label = label
        
        # Threshold for unknown (tuned heuristic)
        if min_dist > 0.3: 
            return "UNKNOWN", min_dist
            
        return best_label, min_dist

# ================= MAIN =================
def main():
    classifier = SimpleClassifier()
    classifier.load_training_data()
    
    if not classifier.centroids:
        print("❌ No classes trained. Please collect data first using Collectdata.py!")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((UDP_IP, UDP_PORT))
    except OSError:
        print(f"❌ Error: Port {UDP_PORT} is busy. Stop the backend/logger first!")
        return

    print("\n💡 STARTING LIVE CLASSIFICATION (Press Ctrl+C to stop)")
    print("-" * 50)
    
    try:
        while True:
            data, _ = sock.recvfrom(2048)
            message = data.decode("utf-8", errors="ignore").strip()

            if "FLEX:" in message:
                parts = message.split('|')
                flex_str = parts[0].split(':')[1]
                flex_vals = [float(x) for x in flex_str.split(',')]

                label, dist = classifier.predict(flex_vals)
                
                # Visual Bar
                bar = "=" * int((1.0 - min(dist, 1.0)) * 20)
                
                print(f"\rDetected: {label: <10} (Dist: {dist:.3f}) [{bar: <20}]", end="")

    except KeyboardInterrupt:
        print("\n\nStopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
