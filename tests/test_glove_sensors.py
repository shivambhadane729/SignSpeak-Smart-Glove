import serial
import serial.tools.list_ports
import time
import sys

def get_esp32_port():
    """Finds ESP32 port with auto-detect or manual fallback"""
    print("Scanning for serial ports...")
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("❌ No serial ports found automatically.")
        # Ask user for manual input
        val = input("Enter COM port manually (e.g. COM3) or 'q' to quit: ").strip()
        if val.lower() == 'q':
            return None
        return val

    print(f"Found {len(ports)} ports:")
    for i, p in enumerate(ports):
        print(f"  [{i+1}] {p.device}: {p.description}")

    # Auto-select likely candidates
    candidates = []
    for i, p in enumerate(ports):
        if "USB" in p.description or "CP210" in p.description or "CH340" in p.description:
            candidates.append(p)
    
    if candidates:
        print(f"\nAuto-selecting likely ESP32: {candidates[0].device}")
        return candidates[0].device
    
    # Fallback to selection
    val = input("\nSelect port number (1-N) or enter COM name manually: ").strip()
    if val.isdigit():
        idx = int(val) - 1
        if 0 <= idx < len(ports):
            return ports[idx].device
    return val

def main():
    print("=== SignSpeak Glove Sensor Test (Interactive) ===")
    
    port = get_esp32_port()
    if not port:
        print("Aborted.")
        return

    print(f"Attempting to connect to {port} at 115200 baud...")

    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"✅ CONNECTED to {port}!")
        print("Waiting for data... (Press Ctrl+C to stop)")
        print("-" * 60)
        
        while True:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if not line:
                        continue
                    
                    # Print raw line for debugging
                    # print(f"RAW: {line}")
                    
                    # Parse: FLEX:f1,f2,f3,f4 | ACC:ax,ay,az | GYR:gx,gy,gz
                    if "FLEX:" in line and "| ACC:" in line:
                        try:
                            parts = line.split('|')
                            
                            # Extract parts safely
                            flex_part = parts[0].split(':')[1].strip()
                            acc_part = parts[1].split(':')[1].strip()
                            gyr_part = parts[2].split(':')[1].strip()

                            flex_vals = [f"{float(x):.2f}" for x in flex_part.split(',')]
                            acc_vals = [f"{float(x):.2f}" for x in acc_part.split(',')]
                            
                            # Nice formatted output
                            print(f"🖐 FLEX: {flex_vals}  |  📐 ACC: {acc_vals}")
                            
                        except (ValueError, IndexError) as e:
                            print(f"⚠ Parse Error: {e} | Line: {line}")
                    else:
                         print(f"RAW (Unknown format): {line}")

            except KeyboardInterrupt:
                print("\nStopping...")
                break
            except Exception as e:
                print(f"\n❌ Read Error: {e}")
                break
                
        ser.close()
        print("Connection closed.")

    except serial.SerialException as e:
        print(f"\n❌ Connection Failed: {e}")
        print("Make sure the port is correct and not used by another program (like the backend or Arduino IDE).")

if __name__ == "__main__":
    main()
