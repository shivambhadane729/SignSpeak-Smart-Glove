import socket
import socketserver

UDP_PORT = 4210

def get_local_ip():
    try:
        # Create a dummy socket to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) # Doesn't actually connect
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def run_server():
    local_ip = get_local_ip()
    print("="*60)
    print("   🖐 SignSpeak Glove UDP Receiver")
    print("="*60)
    print(f"✅ Listening on: 0.0.0.0:{UDP_PORT}")
    print(f"👉 YOUR COMPUTER IP IS: {local_ip}")
    print(f"👉 MAKE SURE TO UPDATE 'udpAddress' in esp32.ino to: \"{local_ip}\"")
    print("-"*60)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            line = data.decode('utf-8').strip()
            
            # Simple pretty print
            # "FLEX:f1,f2... | ACC:..."
            print(f"[{addr[0]}] {line}")
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        sock.close()

if __name__ == "__main__":
    run_server()
