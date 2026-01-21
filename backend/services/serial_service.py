import serial
import serial.tools.list_ports
import threading
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SerialService:
    def __init__(self, port=None, baud_rate=115200):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.running = False
        self.latest_data = {
            "ax": 0, "ay": 0, "az": 0,
            "gx": 0, "gy": 0, "gz": 0,
            "flex": [0, 0, 0, 0, 0]
        }
        self.thread = None
        self.lock = threading.Lock()

    def _find_esp32_port(self):
        """Auto-detect a likely ESP32/Arduino port"""
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            # Look for common USB-Serial descriptions
            if "USB" in p.description or "Serial" in p.description or "CP210" in p.description or "CH340" in p.description:
                return p.device
        # Fallback to first available if any
        if ports:
            return ports[0].device
        return "COM10" # Default fallback

    def start(self):
        if self.running:
            return
        
        target_port = self.port if self.port else self._find_esp32_port()
        
        try:
            self.ser = serial.Serial(target_port, self.baud_rate, timeout=1)
            self.running = True
            self.thread = threading.Thread(target=self._read_loop, daemon=True)
            self.thread.start()
            logger.info(f"✅ SERIAL CONNECTED: {target_port} @ {self.baud_rate}")
        except serial.SerialException as e:
            logger.error(f"❌ SERIAL ERROR: Could not connect to {target_port}: {e}")
            # Try to list available ports to help user
            ports = [p.device for p in serial.tools.list_ports.comports()]
            logger.info(f"Available ports: {ports}")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.ser:
            self.ser.close()

    def _read_loop(self):
        while self.running and self.ser and self.ser.is_open:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if not line:
                    continue
                
                # Expected format: "f1,f2,f3,ax,ay,az,gx,gy,gz" (9 values)
                parts = line.split(',')
                if len(parts) == 9:
                    with self.lock:
                        # Flex sensors (first 3)
                        self.latest_data["flex"] = [float(x) for x in parts[:3]]
                        
                        # IMU data (next 6)
                        self.latest_data["ax"] = float(parts[3])
                        self.latest_data["ay"] = float(parts[4])
                        self.latest_data["az"] = float(parts[5])
                        self.latest_data["gx"] = float(parts[6])
                        self.latest_data["gy"] = float(parts[7])
                        self.latest_data["gz"] = float(parts[8])
                        self.latest_data["ay"] = float(parts[6])
                        self.latest_data["az"] = float(parts[7])
                        self.latest_data["gx"] = float(parts[8])
                        self.latest_data["gy"] = float(parts[9])
                        self.latest_data["gz"] = float(parts[10])
                        
            except ValueError:
                continue # Ignore parse errors
            except serial.SerialException:
                logger.error("Serial connection lost")
                break
            except Exception as e:
                logger.error(f"Error in serial loop: {e}")
                time.sleep(1)

    def get_data(self):
        with self.lock:
            return self.latest_data.copy()

# Global instance
serial_service = SerialService()
