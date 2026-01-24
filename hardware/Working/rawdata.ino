#include <Wire.h>
#include <MPU6050.h>
#include <WiFi.h>

// ================= WIFI CONFIG =================
const char* ssid = "ESP32_NET";
const char* password = "12345678";

// ================= MPU6050 =================
MPU6050 mpu(0x68);   // confirmed address

// ================= FLEX SENSORS =================
const int FLEX_COUNT = 4;
const int flexPins[FLEX_COUNT] = {34, 35, 32, 33};
int flexVal[FLEX_COUNT];

// ================= MPU VALUES =================
int16_t ax, ay, az;
int16_t gx, gy, gz;

// =================================================
void connectWiFi() {
  Serial.print("Connecting to WiFi");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi CONNECTED");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("--------------------------------");
}

// =================================================
void setup() {
  Serial.begin(115200);
  delay(1500);

  Serial.println("GLOVE START");

  // ---- WIFI ----
  connectWiFi();

  // ---- I2C ----
  Wire.begin(21, 22);
  delay(100);

  // ---- MPU ----
  mpu.initialize();
  delay(100);
  mpu.setSleepEnabled(false);
  delay(100);

  Serial.println("MPU READY");
  Serial.println("STARTING SENSOR STREAM");
  Serial.println("--------------------------------");
}

// =================================================
void loop() {
  // ---- FLEX READ ----
  for (int i = 0; i < FLEX_COUNT; i++) {
    flexVal[i] = analogRead(flexPins[i]);
  }

  // ---- MPU READ ----
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // ---- OUTPUT (SERIAL STREAM) ----
  Serial.print("FLEX:");
  for (int i = 0; i < FLEX_COUNT; i++) {
    Serial.print(flexVal[i]);
    if (i < FLEX_COUNT - 1) Serial.print(",");
  }

  Serial.print(" | ACC:");
  Serial.print(ax); Serial.print(",");
  Serial.print(ay); Serial.print(",");
  Serial.print(az);

  Serial.print(" | GYR:");
  Serial.print(gx); Serial.print(",");
  Serial.print(gy); Serial.print(",");
  Serial.print(gz);

  Serial.println();

  delay(50); // ~20 Hz (good for gestures)
}
