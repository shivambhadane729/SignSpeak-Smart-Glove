// ============================================
// ESP32 FLEX SENSOR TEST CODE
// Reads RAW ADC values from 4 flex sensors
// ============================================

// FLEX SENSOR PINS (ADC1 ONLY)
#define FLEX_INDEX 32
#define FLEX_MIDDLE 35
#define FLEX_RING 34
#define FLEX_PINKY 33

void setup()
{
    Serial.begin(115200);

    // ESP32 ADC configuration
    analogReadResolution(12);       // 0–4095
    analogSetAttenuation(ADC_11db); // Full 3.3V range

    Serial.println("ESP32 Flex Sensor Test Started");
    Serial.println("Index Middle Ring Pinky");
}

void loop()
{
    int index = analogRead(FLEX_INDEX);
    int middle = analogRead(FLEX_MIDDLE);
    int ring = analogRead(FLEX_RING);
    int pinky = analogRead(FLEX_PINKY);

    Serial.print(index);
    Serial.print(" ");
    Serial.print(middle);
    Serial.print(" ");
    Serial.print(ring);
    Serial.print(" ");
    Serial.println(pinky);

    delay(300);
}