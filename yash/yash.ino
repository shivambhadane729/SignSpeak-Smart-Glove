#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

// Configuration
const int flexPins[] = {34, 35, 32, 33}; // Index, Middle, Ring, Pinky
const int WINDOW_SIZE = 15; 
int filterBuffer[4][WINDOW_SIZE];
int writeIdx = 0;

void setup() {
  Serial.begin(115200);
  delay(1000); // Give serial time to start
  Serial.println("\n--- SignSpeak System Starting ---");

  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Warning: MPU6050 not found! Check GPIO 21/22. Continuing with Flex only...");
  } else {
    Serial.println("MPU6050 Ready.");
  }

  analogReadResolution(12); // ESP32 0-4095 range
  
  // Initialize filter buffer with current readings
  for(int f=0; f<4; f++) {
    int startVal = analogRead(flexPins[f]);
    for(int i=0; i<WINDOW_SIZE; i++) filterBuffer[f][i] = startVal;
  }
}

int getSmoothFlex(int idx) {
  int raw = analogRead(flexPins[idx]);
  
  // Logic for Middle Finger (GPIO 35) - 0 when straight, increases when bent
  // We flip it so ALL sensors are High when straight, Low when bent
  if (idx == 1) {
    raw = 4095 - raw; 
  }

  filterBuffer[idx][writeIdx] = raw;
  long sum = 0;
  for (int i = 0; i < WINDOW_SIZE; i++) sum += filterBuffer[idx][i];
  return sum / WINDOW_SIZE;
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Output: F1,F2,F3,F4,AccX,AccY,AccZ
  // This clean CSV format is what the Python script expects
  Serial.print(getSmoothFlex(0)); Serial.print(",");
  Serial.print(getSmoothFlex(1)); Serial.print(",");
  Serial.print(getSmoothFlex(2)); Serial.print(",");
  Serial.print(getSmoothFlex(3)); Serial.print(",");
  Serial.print(a.acceleration.x); Serial.print(",");
  Serial.print(a.acceleration.y); Serial.print(",");
  Serial.println(a.acceleration.z);

  writeIdx = (writeIdx + 1) % WINDOW_SIZE;
  delay(30); // Stable 33Hz sampling rate
}
