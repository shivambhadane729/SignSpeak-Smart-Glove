#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu(0x68);   // confirmed by scanner

// -------- FLEX SENSORS --------
const int FLEX_COUNT = 4;
const int flexPins[FLEX_COUNT] = {34, 35, 32, 33};
int flexVal[FLEX_COUNT];

// -------- MPU VALUES --------
int16_t ax, ay, az;
int16_t gx, gy, gz;

// -------- BUTTON --------
const int buttonPin = 25;

void setup() {
  Serial.begin(115200);
  delay(1500);

  Serial.println("SYSTEM START");

  // ---- I2C INIT (VERY IMPORTANT ORDER) ----
  Wire.begin(21, 22);
  delay(100);

  // ---- MPU INIT ----
  mpu.initialize();
  delay(100);

  // ---- FORCE WAKE MPU ----
  mpu.setSleepEnabled(false);
  delay(100);

  Serial.println("MPU INIT DONE");
  Serial.println("STARTING SENSOR READ");
  Serial.println("--------------------------------");

  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  // ---- READ FLEX ----
  for (int i = 0; i < FLEX_COUNT; i++) {
    flexVal[i] = analogRead(flexPins[i]);
  }

  // ---- READ MPU ----
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // ---- PRINT FLEX ----
  Serial.print("FLEX: ");
  for (int i = 0; i < FLEX_COUNT; i++) {
    Serial.print(flexVal[i]);
    if (i < FLEX_COUNT - 1) Serial.print(", ");
  }
  Serial.println();

  // ---- PRINT MPU ----
  Serial.print("ACC: ");
  Serial.print(ax); Serial.print(", ");
  Serial.print(ay); Serial.print(", ");
  Serial.println(az);

  Serial.print("GYR: ");
  Serial.print(gx); Serial.print(", ");
  Serial.print(gy); Serial.print(", ");
  Serial.println(gz);

  // ---- BUTTON ----
  Serial.print("BUTTON: ");
  Serial.println(digitalRead(buttonPin) == LOW ? "PRESSED" : "RELEASED");

  Serial.println("--------------------------------");
  delay(500);
}
