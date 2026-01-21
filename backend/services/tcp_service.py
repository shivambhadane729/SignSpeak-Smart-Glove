import socket
import threading
import logging
from services.data_store import data_store

logger = logging.getLogger(__name__)

class TcpService:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.running = True
            
            self.thread = threading.Thread(target=self._accept_loop, daemon=True)
            self.thread.start()
            logger.info(f"✅ TCP SERVER LISTENING on {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"❌ TCP START ERROR: {e}")

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()

    def _accept_loop(self):
        while self.running:
            try:
                client_sock, addr = self.server_socket.accept()
                print(f"📱 ESP32 CONNECTED from {addr}") # DEBUG PRINT
                logger.info(f"📱 ESP32 CONNECTED from {addr}")
                self._handle_client(client_sock)
            except OSError:
                if self.running:
                    logger.error("TCP Accept failed")
                break

    def _handle_client(self, conn):
        buffer = ""
        try:
            while self.running:
                data = conn.recv(1024).decode(errors="ignore")
                if not data:
                    break
                
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line:
                        # logger.info(f"raw: {line}") # Uncomment for extreme debug
                        if len(line) > 0: print(f"RAW: {line}") # DEBUG PRINT
                        self._parse_line(line)
        except Exception as e:
            logger.error(f"TCP Error: {e}")
        finally:
            conn.close()
            logger.info("📱 ESP32 DISCONNECTED")

    def _parse_line(self, line):
        try:
            # Expected: f1,f2,f3,ax,ay,az,gx,gy,gz (9 values)
            parts = line.split(',')
            
            # Support both 9 (3 Flex) and 11 (5 Flex) formats
            if len(parts) == 9:
                flex_raw = [float(x) for x in parts[:3]]
                # Map 3 sensors to 5-slot array
                # Assuming setup: [Thumb, Index, Middle, Ring, Pinky]
                # Firmware sends: [Flex1, Flex2, Flex3]
                # Map to: [0, Flex1, Flex2, Flex3, 0] (Adjust as needed!)
                flex = [flex_raw[0], flex_raw[1], flex_raw[2], 0, 0] 

                imu = [float(x) for x in parts[3:]]
                
                data_store.update({
                    "flex": flex,
                    "ax": imu[0], "ay": imu[1], "az": imu[2],
                    "gx": imu[3], "gy": imu[4], "gz": imu[5]
                })

            elif len(parts) == 11:
                flex = [float(x) for x in parts[:5]]
                imu = [float(x) for x in parts[5:]]
                
                data_store.update({
                    "flex": flex,
                    "ax": imu[0], "ay": imu[1], "az": imu[2],
                    "gx": imu[3], "gy": imu[4], "gz": imu[5]
                })

        except ValueError:
            pass # Ignore corrupt packets

# Global Instance
tcp_service = TcpService()
