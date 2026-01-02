# Hardware Components List

## Required Components for SignSpeak Smart Glove

### Core Components

1. **ESP32 Development Board** (1x)
   - Microcontroller with built-in Bluetooth
   - Recommended: ESP32 DevKit V1 or similar
   - Price: ~$5-10

2. **Flex Sensors** (5x)
   - Analog flex sensors for finger bending detection
   - Recommended: 2.2" flex sensors (SparkFun SEN-08606 or similar)
   - Price: ~$10-15 each

3. **MPU6050 IMU Module** (1x)
   - 6-axis accelerometer and gyroscope
   - I2C interface
   - Price: ~$2-5

4. **Li-Ion Battery** (1x)
   - 1200mAh capacity (or higher)
   - 3.7V nominal voltage
   - Price: ~$5-10

5. **Battery Charging Module** (1x)
   - TP4056 or similar Li-Ion charger
   - USB-C or Micro-USB input
   - Price: ~$2-3

### Supporting Components

6. **Resistors** (5x)
   - 10kΩ pull-down resistors for flex sensors
   - 1/4W or 1/2W rating
   - Price: ~$1

7. **Jumper Wires** (Multiple)
   - Male-to-male and male-to-female
   - For connections between components
   - Price: ~$3-5

8. **Breadboard or PCB** (1x)
   - For prototyping or final assembly
   - Price: ~$2-10

9. **Glove** (1x)
   - Fabric glove for mounting sensors
   - Price: ~$5-15

10. **3D Printed Enclosure** (Optional)
    - For battery and ESP32 protection
    - Price: ~$5-20 (if printed)

### Tools Required

- Soldering iron and solder (for permanent connections)
- Wire strippers
- Multimeter (for testing)
- Arduino IDE (software)

## Total Estimated Cost

**Basic Version**: ~$80-120 USD
**Professional Version** (with enclosure): ~$100-150 USD

## Where to Buy

- **SparkFun Electronics**: https://www.sparkfun.com
- **Adafruit**: https://www.adafruit.com
- **Amazon**: Search for "ESP32", "flex sensor", "MPU6050"
- **AliExpress**: For budget components (longer shipping)

## Assembly Notes

1. Flex sensors should be mounted on the back of each finger
2. MPU6050 should be mounted on the back of the hand
3. ESP32 and battery can be mounted on the wrist or forearm
4. Ensure all connections are secure before powering on
5. Test each sensor individually before final assembly

## Safety Considerations

- Use proper battery protection circuits
- Avoid short circuits
- Test with low voltage first
- Follow proper soldering safety procedures

