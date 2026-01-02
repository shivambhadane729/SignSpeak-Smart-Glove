/*
 * SignSpeak Smart Glove - ESP32 Firmware
 * 
 * Hardware Connections:
 * - 5 Flex Sensors: A0, A1, A2, A3, A4 (analog inputs)
 * - MPU6050 IMU: SDA (GPIO21), SCL (GPIO22) - I2C
 * - Bluetooth: Built-in ESP32 Bluetooth Serial
 * 
 * Sampling Rate: 20Hz (50ms intervals)
 */

#include <Wire.h>
#include <MPU6050.h>
#include <BluetoothSerial.h>

// Check if Bluetooth is available
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to enable it
#endif

// Bluetooth Serial object
BluetoothSerial SerialBT;

// MPU6050 object
MPU6050 mpu;

// Flex sensor pins (analog inputs)
const int FLEX_PINS[5] = {A0, A1, A2, A3, A4};
const int NUM_FLEX_SENSORS = 5;

// Sampling configuration
const unsigned long SAMPLE_INTERVAL_MS = 50; // 20Hz = 50ms
unsigned long lastSampleTime = 0;

// Data packet structure
struct SensorData {
  unsigned long timestamp;
  int flexValues[5];
  int16_t accelX, accelY, accelZ;
  int16_t gyroX, gyroY, gyroZ;
};

SensorData sensorData;

void setup() {
  // Initialize Serial for debugging
  Serial.begin(115200);
  delay(1000);
  
  // Initialize Bluetooth Serial
  SerialBT.begin("SignSpeak_Glove"); // Bluetooth device name
  Serial.println("Bluetooth device ready! Pair with 'SignSpeak_Glove'");
  
  // Initialize I2C for MPU6050
  Wire.begin();
  delay(100);
  
  // Initialize MPU6050
  Serial.println("Initializing MPU6050...");
  if (!mpu.begin()) {
    Serial.println("MPU6050 initialization failed!");
    while (1) {
      delay(1000);
    }
  }
  
  // Configure MPU6050
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  
  Serial.println("MPU6050 initialized successfully!");
  
  // Initialize analog pins for flex sensors
  for (int i = 0; i < NUM_FLEX_SENSORS; i++) {
    pinMode(FLEX_PINS[i], INPUT);
  }
  
  Serial.println("SignSpeak Glove initialized!");
  Serial.println("Starting data transmission...");
  
  lastSampleTime = millis();
}

void loop() {
  unsigned long currentTime = millis();
  
  // Check if it's time to sample (20Hz = 50ms intervals)
  if (currentTime - lastSampleTime >= SAMPLE_INTERVAL_MS) {
    // Read all sensors
    readSensors();
    
    // Transmit data via Bluetooth
    transmitData();
    
    lastSampleTime = currentTime;
  }
  
  // Small delay to prevent watchdog issues
  delay(1);
}

void readSensors() {
  // Update timestamp
  sensorData.timestamp = millis();
  
  // Read flex sensors (12-bit ADC: 0-4095)
  for (int i = 0; i < NUM_FLEX_SENSORS; i++) {
    sensorData.flexValues[i] = analogRead(FLEX_PINS[i]);
  }
  
  // Read MPU6050 IMU data
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);
  
  // Convert to integers (multiply by 100 to preserve 2 decimal places)
  sensorData.accelX = (int16_t)(accel.acceleration.x * 100);
  sensorData.accelY = (int16_t)(accel.acceleration.y * 100);
  sensorData.accelZ = (int16_t)(accel.acceleration.z * 100);
  
  sensorData.gyroX = (int16_t)(gyro.gyro.x * 100);
  sensorData.gyroY = (int16_t)(gyro.gyro.y * 100);
  sensorData.gyroZ = (int16_t)(gyro.gyro.z * 100);
}

void transmitData() {
  // Format: TIMESTAMP,FLEX0,FLEX1,FLEX2,FLEX3,FLEX4,ACCX,ACCY,ACCZ,GYRX,GYRY,GYRZ\n
  SerialBT.print(sensorData.timestamp);
  SerialBT.print(",");
  
  for (int i = 0; i < NUM_FLEX_SENSORS; i++) {
    SerialBT.print(sensorData.flexValues[i]);
    if (i < NUM_FLEX_SENSORS - 1) SerialBT.print(",");
  }
  SerialBT.print(",");
  
  SerialBT.print(sensorData.accelX);
  SerialBT.print(",");
  SerialBT.print(sensorData.accelY);
  SerialBT.print(",");
  SerialBT.print(sensorData.accelZ);
  SerialBT.print(",");
  
  SerialBT.print(sensorData.gyroX);
  SerialBT.print(",");
  SerialBT.print(sensorData.gyroY);
  SerialBT.print(",");
  SerialBT.print(sensorData.gyroZ);
  SerialBT.print("\n");
  
  // Also print to Serial for debugging
  Serial.print("Data: ");
  Serial.print(sensorData.timestamp);
  Serial.print(", Flex: [");
  for (int i = 0; i < NUM_FLEX_SENSORS; i++) {
    Serial.print(sensorData.flexValues[i]);
    if (i < NUM_FLEX_SENSORS - 1) Serial.print(", ");
  }
  Serial.print("], Accel: [");
  Serial.print(sensorData.accelX);
  Serial.print(", ");
  Serial.print(sensorData.accelY);
  Serial.print(", ");
  Serial.print(sensorData.accelZ);
  Serial.print("], Gyro: [");
  Serial.print(sensorData.gyroX);
  Serial.print(", ");
  Serial.print(sensorData.gyroY);
  Serial.print(", ");
  Serial.print(sensorData.gyroZ);
  Serial.println("]");
}

