import socket
import time
import requests
import sys

# CONFIG
Backend_TCP_IP = "127.0.0.1"
Backend_TCP_PORT = 5000
API_URL = "http://127.0.0.1:8000/imu"

# DATA TEMPLATES
# Format: f1,f2,f3,f4,f5,ax,ay,az,gx,gy,gz
# Based on heuristics in sensors.py:
# f1 (mid) < 460 = BENT
# f2 (ring) < 560 = BENT
# OPEN value ~ 600

def create_packet(f1, f2, f3=600, f4=600, f5=600, ax=0, ay=0, az=0, gx=0, gy=0, gz=0):
    return f"{f1},{f2},{f3},{f4},{f5},{ax},{ay},{az},{gx},{gy},{gz}\n"

PATTERNS = {
    "WAITING": create_packet(600, 600),          # All open
    "HELLO":   create_packet(400, 600),          # f1 bent
    "YES":     create_packet(600, 400),          # f2 bent
    "NO":      create_packet(400, 400)           # Both bent
}

LANGUAGES = [
    "en", "hi", "mr", 
    "bn", "gu", "ta", 
    "te", "kn", "ml"
]

def test_system():
    print(f"🚀 STARTING MULTI-LANGUAGE SYSTEM TEST")
    print(f"📡 Connecting to TCP {Backend_TCP_IP}:{Backend_TCP_PORT}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((Backend_TCP_IP, Backend_TCP_PORT))
        print("✅ TCP Connected!")
    except Exception as e:
        print(f"❌ TCP Connection Failed: {e}")
        return

    # TEST LOOP
    for lang in LANGUAGES:
        print(f"\n========================================")
        print(f"🌐 TESTING LANGUAGE: {lang.upper()}")
        print(f"========================================")

        for name, packet in PATTERNS.items():
            print(f"\n--- GESTURE: {name} ---")
            
            # Send a burst of packets
            # print(f"📤 Sending data...") 
            for _ in range(15): # Reduced count for speed
                sock.sendall(packet.encode())
                time.sleep(0.02) 
            
            # Check API
            try:
                # REQUEST WITH LANGUAGE PARAM
                url = f"{API_URL}?lang={lang}&use_gemini=true"
                resp = requests.get(url)
                
                if resp.status_code == 200:
                    data = resp.json()
                    detected = data.get("gesture")
                    sentence = data.get("sentence")
                    
                    print(f"📥 Response: [{detected}] -> \"{sentence}\"")
                    
                    if detected == name:
                        print("✅ GESTURE MATCH")
                    else:
                        print(f"❌ GESTURE MISMATCH (Expected {name})")
                else:
                    print(f"❌ API Error: {resp.status_code}")
            except Exception as e:
                print(f"❌ Request Failed: {e}")
            
            time.sleep(0.5) # Pause between gestures

    print("\n🏁 MULTI-LANGUAGE TEST COMPLETE")
    sock.close()

if __name__ == "__main__":
    test_system()
