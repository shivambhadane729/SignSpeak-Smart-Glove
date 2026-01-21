import threading
import time

class DataStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.latest_data = {
            "ax": 0.0, "ay": 0.0, "az": 0.0,
            "gx": 0.0, "gy": 0.0, "gz": 0.0,
            "flex": [0, 0, 0, 0, 0],
            "last_updated": 0
        }

    def update(self, new_data):
        with self.lock:
            self.latest_data.update(new_data)
            self.latest_data["last_updated"] = time.time()

    def get(self):
        with self.lock:
            return self.latest_data.copy()

# Global Instance
data_store = DataStore()
