// ============================================
// ESP32 SENSOR TEST - NO WIFI / NO SERVER
// 5 Flex Sensors + MPU6050
// Use Serial Monitor (115200 baud) to view data
// ============================================

#include <Wire.h>

// ---------- FLEX SENSOR PINS (ADC1 ONLY) ----------
// Thumb, Index, Middle, Ring, Pinky
const int FLEX_PINS[5] = {36, 32, 35, 34, 33}; 
int flexValues[5];

// ---------- MPU6050 ----------
#define MPU_ADDRESS 0x68
int16_t ax, ay, az, gx, gy, gz;

void setup() {
  Serial.begin(115200);
  while (!Serial); // Wait for Serial to be ready
  
  Serial.println("\n=== ESP32 SENSOR TEST START ===");
  
  // 1. Setup Flex Pins
  for(int i=0; i<5; i++) {
    pinMode(FLEX_PINS[i], INPUT);
    Serial.printf("Flex Pin %d Configured\n", FLEX_PINS[i]);
  }

  // 2. Setup MPU6050
  Wire.begin();
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x6B); // Power Management
  Wire.write(0);    // Wake up
  byte error = Wire.endTransmission(true);
  
  if (error == 0) {
    Serial.println("MPU6050 Connection Successful!");
  } else {
    Serial.print("MPU6050 Connection Failed. Error: ");
    Serial.println(error);
  }
  
  Serial.println("-------------------------------------------------------------");
  Serial.println("F1\tF2\tF3\tF4\tF5\tAX\tAY\tAZ\tGX\tGY\tGZ");
  Serial.println("-------------------------------------------------------------");
}

void loop() {
  // A. Read Flex Sensors
  for (int i=0; i<5; i++) {
    flexValues[i] = analogRead(FLEX_PINS[i]);
  }

  // B. Read MPU6050
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

  // C. Print Data to Serial
  // Format: Tab separated for easy reading
  Serial.print(flexValues[0]); Serial.print("\t");
  Serial.print(flexValues[1]); Serial.print("\t");
  Serial.print(flexValues[2]); Serial.print("\t");
  Serial.print(flexValues[3]); Serial.print("\t");
  Serial.print(flexValues[4]); Serial.print("\t");
  
  Serial.print(ax/16384.0, 2); Serial.print("\t");
  Serial.print(ay/16384.0, 2); Serial.print("\t");
  Serial.print(az/16384.0, 2); Serial.print("\t");
  Serial.print(gx/131.0, 0);   Serial.print("\t");
  Serial.print(gy/131.0, 0);   Serial.print("\t");
  Serial.println(gz/131.0, 0);

  delay(200); // 5Hz mainly for readability
}
