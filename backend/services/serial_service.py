import serial
import serial.tools.list_ports
import threading
import time
import logging
from services.data_store import data_store

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SerialService:
    def __init__(self, port=None, baud_rate=115200):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.running = False
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
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
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

            except (ValueError, IndexError):
                continue # Ignore parse errors (common during startup)
            except serial.SerialException:
                logger.error("Serial connection lost")
                break
            except Exception as e:
                logger.error(f"Error in serial loop: {e}")
                time.sleep(1)

# Global instance
serial_service = SerialService()
