// ============================================
// ESP32 TCP CLIENT - 5 FLEX + MPU6050 (ACCEL + GYRO)
// Sends 11 values to Python TCP Server
// ============================================

#include <WiFi.h>
#include <Wire.h>

// ---------- WI-FI CONFIG (UPDATE THESE) ----------
const char* ssid     = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* host     = "192.168.137.1"; // <--- ENTER YOUR LAPTOP IP HERE
const int port       = 5000;

// ---------- FLEX SENSOR PINS (ADC1 ONLY) ----------
// Thumb, Index, Middle, Ring, Pinky
const int FLEX_PINS[5] = {36, 32, 35, 34, 33}; 
int flexValues[5];

// ---------- MPU6050 ----------
#define MPU_ADDRESS 0x68
int16_t ax, ay, az, gx, gy, gz;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  
  // 1. Setup Flex Pins
  for(int i=0; i<5; i++) {
    pinMode(FLEX_PINS[i], INPUT);
  }

  // 2. Setup MPU6050
  Wire.begin();
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x6B); // Power Management
  Wire.write(0);    // Wake up
  Wire.endTransmission(true);

  // 3. Connect to Wi-Fi
  Serial.println();
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // A. Connect/Reconnect to TCP Server
  if (!client.connected()) {
    Serial.print("Connecting to Server...");
    if (client.connect(host, port)) {
      Serial.println("Connected!");
    } else {
      Serial.println("Failed. Retrying in 2s...");
      // Don't block completely, just wait a bit and continue to read sensors
      delay(2000); 
    }
  }

  // B. Read Flex Sensors
  for (int i=0; i<5; i++) {
    flexValues[i] = analogRead(FLEX_PINS[i]);
  }

  // C. Read MPU6050 (Accel + Gyro)
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDRESS, 14, true);

  if (Wire.available() == 14) {
    ax = Wire.read()<<8 | Wire.read();
    ay = Wire.read()<<8 | Wire.read();
    az = Wire.read()<<8 | Wire.read();
    Wire.read(); Wire.read(); // Temp
    gx = Wire.read()<<8 | Wire.read();
    gy = Wire.read()<<8 | Wire.read();
    gz = Wire.read()<<8 | Wire.read();
  }

  // D. Format Data: f1,f2,f3,f4,f5,ax,ay,az,gx,gy,gz
  String data = "";
  for(int i=0; i<5; i++) {
    data += String(flexValues[i]) + ",";
  }
  data += String(ax/16384.0) + ",";
  data += String(ay/16384.0) + ",";
  data += String(az/16384.0) + ",";
  data += String(gx/131.0) + ",";
  data += String(gy/131.0) + ",";
  data += String(gz/131.0); 

  // E. Send to Server (if connected)
  if (client.connected()) {
    client.println(data);
  }
  
  // F. Print to Serial (for debugging)
  Serial.println(data);

  delay(50); // 20Hz
}
