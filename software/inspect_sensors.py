"""
SignSpeak - Sensor Inspection Tool
Reads raw data from UDP (WiFi) or Serial (USB) and prints it to the console.
Usage: python software/inspect_sensors.py
"""
import socket
import time
import sys

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

def inspect_udp():
    print(f"📡 Listening for UDP data on {UDP_IP}:{UDP_PORT}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(2.0)

    try:
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                line = data.decode('utf-8').strip()
                
                # Expected format: "FLEX:f1,f2,f3,f4 | ACC:ax,ay,az | GYR:gx,gy,gz"
                if "FLEX:" in line:
                    parts = line.split('|')
                    flex = parts[0].strip()
                    acc = parts[1].strip() if len(parts) > 1 else "ACC: N/A"
                    
                    # Parsed values for easier reading
                    flex_vals = flex.split(':')[1]
                    
                    print(f"\r📊 {flex} | {acc}                      ", end="", flush=True)
                else:
                    print(f"\r❓ Unknown format: {line}", end="", flush=True)
                    
            except socket.timeout:
                print("\r⏳ No data received (Timeout)...", end="", flush=True)
    except KeyboardInterrupt:
        print("\n🛑 Stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    inspect_udp()
