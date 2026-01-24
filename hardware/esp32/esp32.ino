#include <Wire.h>
#include <MPU6050.h>
#include <WiFi.h>
#include <WiFiUdp.h>

// ================= WIFI =================
const char* ssid = "ESP32_NET";
const char* password = "12345678";

// ================= UDP =================
WiFiUDP udp;
const char* laptopIP = "192.168.137.1";   // Windows Hotspot Default IP
const int udpPort = 5005;

// ================= MPU =================
MPU6050 mpu(0x68);

// ================= FLEX =================
const int FLEX_COUNT = 4;
const int flexPins[FLEX_COUNT] = {34, 35, 32, 33};

int flexRaw[FLEX_COUNT];
int flexMin[FLEX_COUNT] = {4095, 4095, 4095, 4095};
int flexMax[FLEX_COUNT] = {0, 0, 0, 0};
float flexNorm[FLEX_COUNT];
float flexSmooth[FLEX_COUNT];

// ================= MPU VALUES =================
int16_t ax, ay, az;
int16_t gx, gy, gz;

// Gyro bias
float gyroBiasX = 0, gyroBiasY = 0, gyroBiasZ = 0;

// Smoothed MPU
float accSmooth[3] = {0, 0, 0};
float gyroSmooth[3] = {0, 0, 0};

// ================= PARAMS =================
const float SMOOTH_ALPHA = 0.7;
const int GYRO_CALIB_SAMPLES = 300;
const int ADC_SAMPLES = 10; // Noise Reduction: Average 10 samples

// =================================================
void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

// =================================================
void calibrateGyro() {
  Serial.println("Calibrating Gyro...");
  long sx = 0, sy = 0, sz = 0;

  for (int i = 0; i < GYRO_CALIB_SAMPLES; i++) {
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    sx += gx;
    sy += gy;
    sz += gz;
    delay(5);
  }

  gyroBiasX = (float)sx / GYRO_CALIB_SAMPLES;
  gyroBiasY = (float)sy / GYRO_CALIB_SAMPLES;
  gyroBiasZ = (float)sz / GYRO_CALIB_SAMPLES;
  Serial.println("Calibration Done.");
}

// =================================================
int readFLEX(int pin) {
  long sum = 0;
  for (int i = 0; i < ADC_SAMPLES; i++) {
    sum += analogRead(pin);
    delayMicroseconds(50); // Small delay to decouple reads
  }
  return (int)(sum / ADC_SAMPLES);
}

// =================================================
void setup() {
  Serial.begin(115200);
  delay(1500);

  // ---- WIFI ----
  connectWiFi();

  // ---- UDP ----
  udp.begin(udpPort);

  // ---- I2C ----
  Wire.begin(21, 22);
  delay(100);

  // ---- MPU ----
  mpu.initialize();
  delay(100);
  mpu.setSleepEnabled(false);
  delay(100);

  // ---- GYRO CALIB ----
  calibrateGyro();
}

// =================================================
void loop() {
  // -------- FLEX READ + CALIB --------
  for (int i = 0; i < FLEX_COUNT; i++) {
    // ADC Noise Reduction: Multisampling
    flexRaw[i] = readFLEX(flexPins[i]);
    
    flexMin[i] = min(flexMin[i], flexRaw[i]);
    flexMax[i] = max(flexMax[i], flexRaw[i]);

    if (flexMax[i] != flexMin[i]) {
      flexNorm[i] = (float)(flexRaw[i] - flexMin[i]) /
                    (flexMax[i] - flexMin[i]);
    } else {
      flexNorm[i] = 0.0;
    }

    flexNorm[i] = constrain(flexNorm[i], 0.0, 1.0);

    flexSmooth[i] = SMOOTH_ALPHA * flexSmooth[i] +
                    (1.0 - SMOOTH_ALPHA) * flexNorm[i];
  }

  // -------- MPU READ --------
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  float accX = ax / 16384.0;
  float accY = ay / 16384.0;
  float accZ = az / 16384.0;

  float gyroX = (gx - gyroBiasX) / 2000.0;
  float gyroY = (gy - gyroBiasY) / 2000.0;
  float gyroZ = (gz - gyroBiasZ) / 2000.0;

  accSmooth[0] = SMOOTH_ALPHA * accSmooth[0] + (1 - SMOOTH_ALPHA) * accX;
  accSmooth[1] = SMOOTH_ALPHA * accSmooth[1] + (1 - SMOOTH_ALPHA) * accY;
  accSmooth[2] = SMOOTH_ALPHA * accSmooth[2] + (1 - SMOOTH_ALPHA) * accZ;

  gyroSmooth[0] = SMOOTH_ALPHA * gyroSmooth[0] + (1 - SMOOTH_ALPHA) * gyroX;
  gyroSmooth[1] = SMOOTH_ALPHA * gyroSmooth[1] + (1 - SMOOTH_ALPHA) * gyroY;
  gyroSmooth[2] = SMOOTH_ALPHA * gyroSmooth[2] + (1 - SMOOTH_ALPHA) * gyroZ;

  // -------- BUILD UDP PAYLOAD --------
  String payload = "FLEX:";
  for (int i = 0; i < FLEX_COUNT; i++) {
    payload += String(flexSmooth[i], 3);
    if (i < FLEX_COUNT - 1) payload += ",";
  }

  payload += " | ACC:";
  payload += String(accSmooth[0], 3) + ",";
  payload += String(accSmooth[1], 3) + ",";
  payload += String(accSmooth[2], 3);

  payload += " | GYR:";
  payload += String(gyroSmooth[0], 3) + ",";
  payload += String(gyroSmooth[1], 3) + ",";
  payload += String(gyroSmooth[2], 3);

  // -------- SEND UDP --------
  if (WiFi.status() == WL_CONNECTED) {
    udp.beginPacket(laptopIP, udpPort);
    udp.print(payload);
    udp.endPacket();
  }

  // Serial debug output (optional)
  // Serial.println(payload);

  delay(40); // ~25 Hz
}