import socket
import threading
import logging
import time
from services.data_store import data_store

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UDPService:
    def __init__(self, host="0.0.0.0", port=5005):
        self.host = host
        self.port = port
        self.sock = None
        self.running = False
        self.thread = None
        self.lock = threading.Lock()

    def start(self):
        if self.running:
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.host, self.port))
            # Set timeout to allow check for 'running' flag periodically
            self.sock.settimeout(1.0) 
            
            self.running = True
            self.thread = threading.Thread(target=self._read_loop, daemon=True)
            self.thread.start()
            logger.info(f"✅ UDP SERVICE STARTED: Listening on {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"❌ UDP START ERROR: {e}")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.sock:
            self.sock.close()
        logger.info("UDP SERVICE STOPPED")

    def _read_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                line = data.decode('utf-8', errors='ignore').strip()
                
                if not line:
                    continue

                # Format: "FLEX:f1,f2,f3,f4 | ACC:ax,ay,az | GYR:gx,gy,gz"
                if "FLEX:" in line and "| ACC:" in line:
                    parts = line.split('|')
                    
                    flex_str = parts[0].split(':')[1]
                    acc_str = parts[1].split(':')[1]
                    gyr_str = parts[2].split(':')[1]

                    flex_vals = [float(x) for x in flex_str.split(',')]
                    acc_vals = [float(x) for x in acc_str.split(',')]
                    gyr_vals = [float(x) for x in gyr_str.split(',')]

                    # Update Global Data Store
                    data_store.update({
                        "flex": flex_vals,
                        "ax": acc_vals[0], "ay": acc_vals[1], "az": acc_vals[2],
                        "gx": gyr_vals[0], "gy": gyr_vals[1], "gz": gyr_vals[2]
                    })
                    print(f"RAW DATA | FLEX: {flex_vals} | ACC: {acc_vals} | GYR: {gyr_vals}")
                    
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    logger.error(f"Error in UDP loop: {e}")
                time.sleep(0.1)

# Global instance
udp_service = UDPService()
