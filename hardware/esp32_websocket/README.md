# ESP32 WebSocket Client - Setup Guide

## 📋 Hardware Requirements

- ESP32 Development Board
- MPU6050 IMU Module
- Jumper wires
- USB cable for programming

## 🔌 Wiring Diagram

```
ESP32          MPU6050
------         -------
3.3V    ────>  VCC
GND     ────>  GND
GPIO21  ────>  SDA
GPIO22  ────>  SCL
```

## ⚙️ Configuration

### Step 1: Install Required Libraries

In Arduino IDE:
1. **ESP32 Board Support**: 
   - File → Preferences → Additional Board Manager URLs
   - Add: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
   - Tools → Board → Boards Manager → Search "ESP32" → Install

2. **Required Libraries**:
   - `WebSockets` by Markus Sattler (Install via Library Manager)
   - `MPU6050` by Electronic Cats (Install via Library Manager)

### Step 2: Configure Wi-Fi Credentials

Edit `esp32_mpu6050.ino`:

```cpp
const char* ssid = "YOUR_HOTSPOT_SSID";        // Your laptop hotspot name
const char* password = "YOUR_HOTSPOT_PASSWORD"; // Your hotspot password
```

### Step 3: Verify Server IP

The code is already configured for:
```cpp
const char* ws_host = "192.168.137.1";  // Laptop IP (hotspot)
const int ws_port = 8000;
```

If your laptop uses a different IP, update `ws_host`.

### Step 4: Upload Code

1. Select Board: **Tools → Board → ESP32 Dev Module**
2. Select Port: **Tools → Port → (your ESP32 port)**
3. Click **Upload**

## 🔍 Verification

### Serial Monitor Output

After upload, open Serial Monitor (115200 baud) and you should see:

```
============================================================
  SignSpeak ESP32 - MPU6050 WebSocket Client
============================================================

Initializing MPU6050...
✅ MPU6050 initialized successfully!

📶 Connecting to Wi-Fi: YourHotspot
.................
✅ Wi-Fi connected!
📡 IP Address: 192.168.137.XXX
📶 Signal Strength (RSSI): -45 dBm

✅ WebSocket connected to: ws://192.168.137.1:8000/ws
📤 Sent identification message
📥 Received: {"type":"ack","status":"connected",...}
✅ Server acknowledged connection
```

### Expected Behavior

- ✅ Green LED on ESP32 (if available)
- ✅ Serial output shows connection status
- ✅ Data sent every 50ms (20Hz)
- ✅ Automatic reconnection on Wi-Fi/WebSocket drop

## 🐛 Troubleshooting

### MPU6050 Not Detected

**Symptoms**: "MPU6050 initialization failed!"

**Solutions**:
- Check I2C wiring (SDA=GPIO21, SCL=GPIO22)
- Verify power connections (3.3V, GND)
- Try different MPU6050 module (some are faulty)
- Check I2C address (default: 0x68)

### Wi-Fi Connection Fails

**Symptoms**: "Wi-Fi connection failed!" after 20 attempts

**Solutions**:
- Verify hotspot is enabled on laptop
- Check SSID and password are correct (case-sensitive)
- Ensure ESP32 is within range
- Try resetting hotspot
- Check if hotspot allows device connections

### WebSocket Connection Fails

**Symptoms**: "WebSocket disconnected" or no acknowledgment

**Solutions**:
- Verify backend server is running: `python Web/server.py`
- Check laptop IP is correct: `ipconfig` (Windows) or `ifconfig` (Linux/Mac)
- Check firewall allows port 8000
- Verify WebSocket URL: `ws://192.168.137.1:8000/ws`
- Check backend terminal for connection logs

### No Data Transmission

**Symptoms**: Connected but no data in dashboard

**Solutions**:
- Check Serial Monitor for error messages
- Verify MPU6050 is working (values should change when moving)
- Check JSON format in Serial Monitor
- Verify backend is receiving messages (check backend terminal)
- Check browser console for WebSocket errors (F12)

## 📊 Data Format

ESP32 sends JSON every 50ms:

```json
{
  "type": "data",
  "ax": 0.15,
  "ay": -0.82,
  "az": 9.78,
  "gx": 0.12,
  "gy": -0.45,
  "gz": 0.03
}
```

**Units**:
- Accelerometer: m/s²
- Gyroscope: degrees/second

## ⚡ Performance

- **Sampling Rate**: 20Hz (50ms intervals)
- **Wi-Fi Power**: Low power mode enabled
- **Reconnection**: Automatic (3-5 second intervals)
- **Data Rate**: ~2KB/s
- **Latency**: 25-50ms end-to-end

## 🔧 Advanced Configuration

### Change Sampling Rate

```cpp
const unsigned long SAMPLE_INTERVAL_MS = 50;  // 20Hz
// Change to 25 for 40Hz, 100 for 10Hz, etc.
```

### Change WebSocket Server

```cpp
const char* ws_host = "192.168.1.100";  // Different IP
const int ws_port = 8080;                // Different port
```

### Enable Debug Mode

Add more Serial.println() statements for detailed debugging.

## 📚 Next Steps

After ESP32 is working:
1. ✅ Verify data appears in web dashboard
2. ✅ Test gesture recognition with MPU6050 data
3. ✅ Add flex sensors (if available)
4. ✅ Integrate with ML model
5. ✅ Deploy to production



