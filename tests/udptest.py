import socket
import time

# ================= CONFIG =================
UDP_IP = "0.0.0.0"   # listen on all interfaces
UDP_PORT = 5005

def parse_data(line):
    """
    Parses: "FLEX:f1,f2,f3,f4 | ACC:ax,ay,az | GYR:gx,gy,gz"
    """
    try:
        parts = line.split('|')
        
        # Parse FLEX
        flex_str = parts[0].split(':')[1]
        flex_vals = [f"{float(x):.2f}" for x in flex_str.split(',')]
        
        # Parse ACC
        acc_str = parts[1].split(':')[1]
        acc_vals = [f"{float(x):.2f}" for x in acc_str.split(',')]
        
        # Parse GYR
        gyr_str = parts[2].split(':')[1]
        gyr_vals = [f"{float(x):.2f}" for x in gyr_str.split(',')]
        
        return flex_vals, acc_vals, gyr_vals
    except Exception as e:
        return None, None, None

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind((UDP_IP, UDP_PORT))
        print("="*60)
        print(f"✅ LISTENING FOR ALL SENSORS ON PORT {UDP_PORT}")
        print("="*60)
        print("Waiting for data from ESP32...")

        while True:
            data, addr = sock.recvfrom(2048)
            message = data.decode("utf-8", errors="ignore").strip()

            if "FLEX:" in message:
                flex, acc, gyr = parse_data(message)
                
                if flex:
                    # Clear screen (optional, maybe just print line by line)
                    # print("\033[H\033[J", end="") 
                    print(f"[{addr[0]}]")
                    print(f"   🖐  FLEX: {flex}")
                    print(f"   📐  ACC : {acc}")
                    print(f"   🔄  GYR : {gyr}")
                    print("-" * 40)
                else:
                    print(f"Raw: {message}")

    except OSError as e:
        print(f"❌ Error: {e}")
        print("hint: Make sure the Backend Server is STOPPED.")
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
