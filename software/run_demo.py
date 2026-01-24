"""
SignSpeak - Standalone Demo Runner
Usage: python software/run_demo.py

Logic:
- Listens to UDP (5005)
- Calculates Delta (Movement)
- Triggers Word Sequence: Hello -> I -> am -> Yash...
"""
import socket
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

DEMO_SENTENCE = ["Hello,", "I", "am", "Yash.", "We", "Are", "Team", "Fsociety"]
demo_index = 0
last_values = []
last_trigger = 0
COOLDOWN = 1.0
THRESHOLD = 0.3

def run():
    global demo_index, last_values, last_trigger
    
    print(f"📡 Demo Mode Listening on {UDP_PORT}...")
    print(f"🌊 Threshold: {THRESHOLD} | Cooldown: {COOLDOWN}s")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(0.1)

    try:
        while True:
            try:
                data, _ = sock.recvfrom(1024)
                line = data.decode('utf-8').strip()
                
                # Parse "FLEX:f1,f2... | ACC:ax,ay..."
                if "FLEX:" in line:
                    parts = line.split('|')
                    
                    # Extract Flex
                    f_str = parts[0].split(':')[1]
                    flex = [float(x) for x in f_str.split(',')]
                    
                    # Extract Acc
                    a_str = parts[1].split(':')[1]
                    acc = [float(x) for x in a_str.split(',')]
                    
                    curr = flex + acc
                    
                    if not last_values:
                        last_values = curr
                        continue
                        
                    # Calculate Delta
                    n = min(len(curr), len(last_values))
                    delta = sum(abs(curr[i] - last_values[i]) for i in range(n))
                    last_values = curr
                    
                    # Trigger
                    now = time.time()
                    if delta > THRESHOLD and (now - last_trigger) > COOLDOWN:
                        word = DEMO_SENTENCE[demo_index]
                        print(f"✨ TRIGGER (Delta={delta:.2f}) -> {word}")
                        demo_index = (demo_index + 1) % len(DEMO_SENTENCE)
                        last_trigger = now
                    else:
                        print(f"\r🔹 Delta: {delta:.2f} (Waiting...)", end="", flush=True)

            except socket.timeout:
                pass
            except Exception as e:
                print(f"Error: {e}")
                
    except KeyboardInterrupt:
        print("\n🛑 Stopped")
    finally:
        sock.close()

if __name__ == "__main__":
    run()
