// ============================================
// ARDUINO UNO CODE FOR SIGNALOUD GLOVE
// 4 Flex Sensors (Index, Middle, Ring, Pinky) + MPU6050
// ============================================

#include <Wire.h>

// --- SENSOR PIN CONFIGURATION ---
// CRITICAL: A4 and A5 are I2C (MPU6050), do NOT use for flex sensors!
const int FLEX_INDEX = A0;  // Index finger
const int FLEX_MIDDLE = A1; // Middle finger
const int FLEX_RING = A2;   // Ring finger
const int FLEX_PINKY = A3;  // Pinky finger

const int MPU_ADDRESS = 0x68; // MPU6050 I2C address

// --- CALIBRATION VALUES (RUN CALIBRATION MODE FIRST!) ---
// Flat hand vs closed fist values for each sensor
int FLEX_MIN[4] = {300, 290, 310, 305}; // Adjust after calibration
int FLEX_MAX[4] = {700, 720, 710, 715}; // Adjust after calibration

// --- FILTERING PARAMETERS ---
const int SAMPLE_SIZE = 5;      // Rolling average window
int flexBuffer[4][SAMPLE_SIZE]; // Circular buffers for 4 sensors
int bufferIndex = 0;

// --- MPU6050 DATA ---
int16_t accelX, accelY, accelZ;
int16_t gyroX, gyroY, gyroZ;

// --- TIMING ---
unsigned long lastSendTime = 0;
const int SEND_INTERVAL = 50; // 20Hz sampling rate

void setup()
{
  Serial.begin(115200);
  Wire.begin();

  // Initialize MPU6050
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0);    // Wake up MPU6050
  Wire.endTransmission(true);

  // Configure MPU6050 (optional but recommended)
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x1C); // ACCEL_CONFIG register
  Wire.write(0x00); // ±2g sensitivity
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x1B); // GYRO_CONFIG register
  Wire.write(0x00); // ±250°/s sensitivity
  Wire.endTransmission(true);

  // Initialize flex sensor buffers
  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < SAMPLE_SIZE; j++)
    {
      flexBuffer[i][j] = 0;
    }
  }

  delay(100); // Sensor stabilization
}

void loop()
{
  unsigned long currentTime = millis();

  // Send data at consistent intervals
  if (currentTime - lastSendTime >= SEND_INTERVAL)
  {
    lastSendTime = currentTime;

    // --- READ AND FILTER FLEX SENSORS ---
    int flexPins[4] = {FLEX_INDEX, FLEX_MIDDLE, FLEX_RING, FLEX_PINKY};
    int flexValues[4];

    for (int i = 0; i < 4; i++)
    {
      // Read raw value
      int raw = analogRead(flexPins[i]);

      // Add to circular buffer
      flexBuffer[i][bufferIndex] = raw;

      // Calculate rolling average
      long sum = 0;
      for (int j = 0; j < SAMPLE_SIZE; j++)
      {
        sum += flexBuffer[i][j];
      }
      int smoothed = sum / SAMPLE_SIZE;

      // Map to 0-100 range (normalized)
      flexValues[i] = map(smoothed, FLEX_MIN[i], FLEX_MAX[i], 0, 100);
      flexValues[i] = constrain(flexValues[i], 0, 100);
    }

    // Update buffer index
    bufferIndex = (bufferIndex + 1) % SAMPLE_SIZE;

    // --- READ MPU6050 ACCELEROMETER & GYROSCOPE ---
    Wire.beginTransmission(MPU_ADDRESS);
    Wire.write(0x3B); // Starting register for accel data
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDRESS, 14, true);

    // Read accelerometer (3 axes)
    accelX = (Wire.read() << 8 | Wire.read());
    accelY = (Wire.read() << 8 | Wire.read());
    accelZ = (Wire.read() << 8 | Wire.read());

    // Skip temperature
    Wire.read();
    Wire.read();

    // Read gyroscope (3 axes)
    gyroX = (Wire.read() << 8 | Wire.read());
    gyroY = (Wire.read() << 8 | Wire.read());
    gyroZ = (Wire.read() << 8 | Wire.read());

    // Normalize accelerometer (±2g = ±16384 LSB)
    float accelXg = (accelX / 16384.0) * 100;
    float accelYg = (accelY / 16384.0) * 100;
    float accelZg = (accelZ / 16384.0) * 100;

    // Normalize gyroscope (±250°/s = ±131 LSB/°/s)
    float gyroXdeg = gyroX / 131.0;
    float gyroYdeg = gyroY / 131.0;
    float gyroZdeg = gyroZ / 131.0;

    // --- SEND DATA TO PYTHON (10 VALUES) ---
    // Format: index,middle,ring,pinky,accelX,accelY,accelZ,gyroX,gyroY,gyroZ
    Serial.print(flexValues[0]);
    Serial.print(","); // Index
    Serial.print(flexValues[1]);
    Serial.print(","); // Middle
    Serial.print(flexValues[2]);
    Serial.print(","); // Ring
    Serial.print(flexValues[3]);
    Serial.print(","); // Pinky
    Serial.print(accelXg, 2);
    Serial.print(",");
    Serial.print(accelYg, 2);
    Serial.print(",");
    Serial.print(accelZg, 2);
    Serial.print(",");
    Serial.print(gyroXdeg, 2);
    Serial.print(",");
    Serial.print(gyroYdeg, 2);
    Serial.print(",");
    Serial.println(gyroZdeg, 2);
  }
}

// ============================================
// CALIBRATION MODE
// ============================================
// TO USE: Comment out everything above, uncomment below, upload

/*
void setup() {
  Serial.begin(115200);
  Serial.println("=== FLEX SENSOR CALIBRATION ===");
  Serial.println("Straighten all 4 fingers (FLAT HAND) for 5 seconds...");
  delay(5000);

  int flexPins[4] = {A0, A1, A2, A3}; // Index, Middle, Ring, Pinky
  String fingerNames[4] = {"Index", "Middle", "Ring", "Pinky"};

  // Measure flat hand
  int flatValues[4] = {0, 0, 0, 0};
  for (int i = 0; i < 50; i++) {
    for (int j = 0; j < 4; j++) {
      flatValues[j] += analogRead(flexPins[j]);
    }
    delay(20);
  }

  Serial.println("\nFLAT HAND VALUES (FLEX_MIN):");
  for (int i = 0; i < 4; i++) {
    flatValues[i] /= 50;
    Serial.print(fingerNames[i]);
    Serial.print(" (A"); Serial.print(i); Serial.print("): ");
    Serial.println(flatValues[i]);
  }

  Serial.println("\nNow make a TIGHT FIST for 5 seconds...");
  delay(5000);

  // Measure closed fist
  int bentValues[4] = {0, 0, 0, 0};
  for (int i = 0; i < 50; i++) {
    for (int j = 0; j < 4; j++) {
      bentValues[j] += analogRead(flexPins[j]);
    }
    delay(20);
  }

  Serial.println("\nCLOSED FIST VALUES (FLEX_MAX):");
  for (int i = 0; i < 4; i++) {
    bentValues[i] /= 50;
    Serial.print(fingerNames[i]);
    Serial.print(" (A"); Serial.print(i); Serial.print("): ");
    Serial.println(bentValues[i]);
  }

  Serial.println("\n=== COPY THESE TO MAIN CODE ===");
  Serial.print("int FLEX_MIN[4] = {");
  for (int i = 0; i < 4; i++) {
    Serial.print(flatValues[i]);
    if (i < 3) Serial.print(", ");
  }
  Serial.println("};");

  Serial.print("int FLEX_MAX[4] = {");
  for (int i = 0; i < 4; i++) {
    Serial.print(bentValues[i]);
    if (i < 3) Serial.print(", ");
  }
  Serial.println("};");

  Serial.println("\n✅ Calibration complete!");
}

void loop() {
  // Nothing to do
}
*/