/*
 * SignSpeak Smart Glove - ESP32 WebSocket Client
 * Connects to Wi-Fi and sends MPU6050 data via WebSocket
 * 
 * Hardware:
 * - ESP32 DevKit
 * - MPU6050 (I2C: SDA=GPIO21, SCL=GPIO22)
 * 
 * Configuration:
 * - Wi-Fi SSID: Your laptop hotspot name
 * - WebSocket Server: ws://192.168.137.1:8000/ws
 * - Sampling Rate: ~20Hz (50ms interval)
 */

#include <WiFi.h>
#include <WebSocketsClient.h>
#include <Wire.h>
#include <MPU6050.h>

// ==================== CONFIGURATION ====================
const char* ssid = "YOUR_HOTSPOT_SSID";        // Replace with your hotspot name
const char* password = "YOUR_HOTSPOT_PASSWORD"; // Replace with your hotspot password
const char* ws_host = "192.168.137.1";         // Laptop IP
const int ws_port = 8000;
const char* ws_path = "/ws";

// Sampling configuration
const unsigned long SAMPLE_INTERVAL_MS = 50;   // 20Hz = 50ms
unsigned long lastSampleTime = 0;
// =======================================================

// WebSocket client
WebSocketsClient webSocket;

// MPU6050 sensor
MPU6050 mpu;

// Wi-Fi reconnection
unsigned long lastWiFiReconnectAttempt = 0;
const unsigned long WiFi_RECONNECT_INTERVAL = 5000; // 5 seconds

// WebSocket reconnection
unsigned long lastWSReconnectAttempt = 0;
const unsigned long WS_RECONNECT_INTERVAL = 3000;   // 3 seconds

// Connection status
bool wifiConnected = false;
bool wsConnected = false;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println();
  Serial.println("============================================================");
  Serial.println("  SignSpeak ESP32 - MPU6050 WebSocket Client");
  Serial.println("============================================================");
  Serial.println();
  
  // Initialize I2C for MPU6050
  Wire.begin(21, 22);  // SDA=21, SCL=22
  delay(100);
  
  // Initialize MPU6050
  Serial.println("Initializing MPU6050...");
  if (!mpu.begin()) {
    Serial.println("❌ MPU6050 initialization failed!");
    Serial.println("Please check wiring:");
    Serial.println("  VCC -> 3.3V");
    Serial.println("  GND -> GND");
    Serial.println("  SDA -> GPIO21");
    Serial.println("  SCL -> GPIO22");
    while (1) {
      delay(1000);
    }
  }
  
  // Configure MPU6050
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  
  Serial.println("✅ MPU6050 initialized successfully!");
  Serial.println();
  
  // Connect to Wi-Fi
  connectToWiFi();
  
  // Setup WebSocket
  webSocket.begin(ws_host, ws_port, ws_path);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(WS_RECONNECT_INTERVAL);
  
  Serial.println("Setup complete!");
  Serial.println();
}


void loop() {
  // Handle Wi-Fi reconnection
  if (WiFi.status() != WL_CONNECTED) {
    wifiConnected = false;
    if (millis() - lastWiFiReconnectAttempt > WiFi_RECONNECT_INTERVAL) {
      lastWiFiReconnectAttempt = millis();
      connectToWiFi();
    }
  }
  
  // Handle WebSocket reconnection
  webSocket.loop();
  if (wifiConnected && !wsConnected) {
    if (millis() - lastWSReconnectAttempt > WS_RECONNECT_INTERVAL) {
      lastWSReconnectAttempt = millis();
      Serial.println("🔄 Attempting WebSocket reconnection...");
      webSocket.begin(ws_host, ws_port, ws_path);
      webSocket.onEvent(webSocketEvent);
    }
  }
  
  // Send sensor data at configured interval
  if (wifiConnected && wsConnected) {
    unsigned long currentTime = millis();
    if (currentTime - lastSampleTime >= SAMPLE_INTERVAL_MS) {
      sendSensorData();
      lastSampleTime = currentTime;
    }
  }
  
  delay(10); // Small delay to prevent watchdog issues
}


void connectToWiFi() {
  Serial.print("📶 Connecting to Wi-Fi: ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    Serial.println();
    Serial.println("✅ Wi-Fi connected!");
    Serial.print("📡 IP Address: ");
    Serial.println(WiFi.localIP());
    Serial.print("📶 Signal Strength (RSSI): ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
    Serial.println();
  } else {
    wifiConnected = false;
    Serial.println();
    Serial.println("❌ Wi-Fi connection failed!");
    Serial.println("Please check:");
    Serial.println("  1. Hotspot is enabled");
    Serial.println("  2. SSID and password are correct");
    Serial.println("  3. ESP32 is in range");
    Serial.println();
  }
}


void sendSensorData() {
  // Read MPU6050 data
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);
  
  // Create JSON message
  String json = "{";
  json += "\"type\":\"data\",";
  json += "\"ax\":" + String(accel.acceleration.x, 2) + ",";
  json += "\"ay\":" + String(accel.acceleration.y, 2) + ",";
  json += "\"az\":" + String(accel.acceleration.z, 2) + ",";
  json += "\"gx\":" + String(gyro.gyro.x, 2) + ",";
  json += "\"gy\":" + String(gyro.gyro.y, 2) + ",";
  json += "\"gz\":" + String(gyro.gyro.z, 2);
  json += "}";
  
  // Send via WebSocket
  webSocket.sendTXT(json);
}


void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      wsConnected = false;
      Serial.println("❌ WebSocket disconnected");
      break;
      
    case WStype_CONNECTED:
      wsConnected = true;
      Serial.print("✅ WebSocket connected to: ");
      Serial.println((char*)payload);
      
      // Send identification message
      String idMsg = "{\"type\":\"esp32\",\"device\":\"SignSpeak_ESP32\"}";
      webSocket.sendTXT(idMsg);
      Serial.println("📤 Sent identification message");
      break;
      
    case WStype_TEXT:
      // Handle server response
      Serial.print("📥 Received: ");
      Serial.println((char*)payload);
      
      // Parse acknowledgment
      if (strstr((char*)payload, "ack") != NULL) {
        Serial.println("✅ Server acknowledged connection");
      }
      break;
      
    case WStype_ERROR:
      wsConnected = false;
      Serial.print("❌ WebSocket error: ");
      Serial.println((char*)payload);
      break;
      
    default:
      break;
  }
}



