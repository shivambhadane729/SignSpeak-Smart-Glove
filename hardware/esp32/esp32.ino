// ============================================
// ESP32 CODE FOR SIGNALOUD SMART GLOVE
// 4 Flex Sensors (ADC1) + MPU6050
// ============================================

#include <Wire.h>

// ---------- FLEX SENSOR PINS (ADC1 ONLY) ----------
#define FLEX_INDEX   32
#define FLEX_MIDDLE  35
#define FLEX_RING    34
#define FLEX_PINKY   33

// ---------- MPU6050 ----------
#define MPU_ADDRESS 0x68
#define SDA_PIN 21
#define SCL_PIN 22

// ---------- CALIBRATION VALUES (UPDATE AFTER CALIBRATION) ----------
int FLEX_MIN[4] = {1200, 1150, 1180, 1170};
int FLEX_MAX[4] = {3200, 3300, 3250, 3280};

// ---------- FILTERING ----------
const int SAMPLE_SIZE = 5;
int flexBuffer[4][SAMPLE_SIZE];
int bufferIndex = 0;

// ---------- MPU DATA ----------
int16_t accelX, accelY, accelZ;
int16_t gyroX, gyroY, gyroZ;

// ---------- TIMING ----------
unsigned long lastSendTime = 0;
const int SEND_INTERVAL = 50;  // 20 Hz

// ==================================================
// SETUP
// ==================================================
void setup() {
  Serial.begin(115200);

  // ---- ESP32 ADC CONFIG ----
  analogReadResolution(12);          // 0–4095
  analogSetAttenuation(ADC_11db);    // Full 3.3V range

  // ---- I2C INIT ----
  Wire.begin(SDA_PIN, SCL_PIN);

  // ---- MPU6050 INIT ----
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x6B);     // Power management
  Wire.write(0x00);     // Wake up
  Wire.endTransmission(true);

  // Accelerometer ±2g
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x1C);
  Wire.write(0x00);
  Wire.endTransmission(true);

  // Gyroscope ±250°/s
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x1B);
  Wire.write(0x00);
  Wire.endTransmission(true);

  // Init flex buffers
  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < SAMPLE_SIZE; j++) {
      flexBuffer[i][j] = 0;
    }
  }

  delay(200);
}

// ==================================================
// LOOP
// ==================================================
void loop() {
  if (millis() - lastSendTime >= SEND_INTERVAL) {
    lastSendTime = millis();

    int flexPins[4] = {FLEX_INDEX, FLEX_MIDDLE, FLEX_RING, FLEX_PINKY};
    int flexValues[4];

    // ---------- FLEX SENSOR READ ----------
    for (int i = 0; i < 4; i++) {
      int raw = analogRead(flexPins[i]);
      flexBuffer[i][bufferIndex] = raw;

      long sum = 0;
      for (int j = 0; j < SAMPLE_SIZE; j++) {
        sum += flexBuffer[i][j];
      }

      int smooth = sum / SAMPLE_SIZE;

      // ---- SAFETY CHECK FOR BAD CALIBRATION ----
      if (FLEX_MAX[i] - FLEX_MIN[i] < 100) {
        flexValues[i] = 0;
      } else {
        flexValues[i] = map(smooth, FLEX_MIN[i], FLEX_MAX[i], 0, 100);
        flexValues[i] = constrain(flexValues[i], 0, 100);
      }
    }

    bufferIndex = (bufferIndex + 1) % SAMPLE_SIZE;

    // ---------- MPU6050 READ ----------
    Wire.beginTransmission(MPU_ADDRESS);
    Wire.write(0x3B);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDRESS, 14, true);

    accelX = Wire.read() << 8 | Wire.read();
    accelY = Wire.read() << 8 | Wire.read();
    accelZ = Wire.read() << 8 | Wire.read();

    Wire.read(); Wire.read(); // temperature discard

    gyroX = Wire.read() << 8 | Wire.read();
    gyroY = Wire.read() << 8 | Wire.read();
    gyroZ = Wire.read() << 8 | Wire.read();

    // ---------- NORMALIZATION ----------
    float accelXg = (accelX / 16384.0) * 100.0;
    float accelYg = (accelY / 16384.0) * 100.0;
    float accelZg = (accelZ / 16384.0) * 100.0;

    float gyroXdeg = gyroX / 131.0;
    float gyroYdeg = gyroY / 131.0;
    float gyroZdeg = gyroZ / 131.0;

    // ---------- SERIAL OUTPUT ----------
    Serial.print(flexValues[0]); Serial.print(",");
    Serial.print(flexValues[1]); Serial.print(",");
    Serial.print(flexValues[2]); Serial.print(",");
    Serial.print(flexValues[3]); Serial.print(",");
    Serial.print(accelXg, 2); Serial.print(",");
    Serial.print(accelYg, 2); Serial.print(",");
    Serial.print(accelZg, 2); Serial.print(",");
    Serial.print(gyroXdeg, 2); Serial.print(",");
    Serial.print(gyroYdeg, 2); Serial.print(",");
    Serial.println(gyroZdeg, 2);
  }
}

