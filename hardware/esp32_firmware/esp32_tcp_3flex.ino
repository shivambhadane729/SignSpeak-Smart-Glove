// ======================================================
// ESP32 SMART GLOVE - WIFI + TCP CLIENT (FIXED)
// ======================================================

#include <Wire.h>
#include <WiFi.h>

// -------- WIFI CONFIG --------
const char* ssid     = "ESP32_NET";
const char* password = "12345678";
const char* host     = "192.168.137.1";
const int port       = 5000;

// -------- FLEX --------
const int FLEX_PINS[3] = {35, 34, 33};
int flex[3];

// -------- MPU6050 --------
#define MPU_ADDRESS 0x68
int16_t ax, ay, az, gx, gy, gz;

// -------- TIMING --------
unsigned long lastRead = 0;
const unsigned long interval = 10; // 20 Hz

WiFiClient client;
unsigned long lastConnectAttempt = 0;

void setup() {
  Serial.begin(115200);

  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  Wire.begin();
  Wire.setClock(400000);
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void loop() {
  unsigned long now = millis();

  // -------- NON-BLOCKING TCP CONNECT --------
  if (!client.connected() && now - lastConnectAttempt > 2000) {
    lastConnectAttempt = now;
    client.connect(host, port);
  }

  // -------- SENSOR LOOP --------
  if (now - lastRead >= interval) {
    lastRead = now;

    // FLEX
    for (int i = 0; i < 3; i++) {
      flex[i] = analogRead(FLEX_PINS[i]);
    }

    // MPU
    Wire.beginTransmission(MPU_ADDRESS);
    Wire.write(0x3B);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDRESS, 14, true);

    if (Wire.available() == 14) {
      ax = Wire.read()<<8 | Wire.read();
      ay = Wire.read()<<8 | Wire.read();
      az = Wire.read()<<8 | Wire.read();
      Wire.read(); Wire.read();
      gx = Wire.read()<<8 | Wire.read();
      gy = Wire.read()<<8 | Wire.read();
      gz = Wire.read()<<8 | Wire.read();
    }

    // -------- FAST SEND (NO STRING) --------
    char buffer[128];
    snprintf(buffer, sizeof(buffer),
      "%d,%d,%d,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f",
      flex[0], flex[1], flex[2],
      ax/16384.0, ay/16384.0, az/16384.0,
      gx/131.0, gy/131.0, gz/131.0
    );

    if (client.connected()) {
      client.println(buffer);
    }

    Serial.println(buffer);
  }
}
