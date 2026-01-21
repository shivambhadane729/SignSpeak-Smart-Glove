/*
 * SignSpeak Smart Glove - Wi-Fi Firmware
 * Sends sensor data to backend via HTTP POST/GET
 */

#include <WiFi.h>
#include <HTTPClient.h>

// ---------------- CONFIGURATION ----------------
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Backend Server URL (Replace with your laptop's IP)
// NOTE: Do NOT use "localhost" here. Use your IP, e.g., 192.168.1.5
const char* serverUrl = "http://192.168.1.100:8000/data"; 

// Pin Definitions
const int FLEX_PINS[5] = {36, 39, 34, 35, 32}; // VP, VN, 34, 35, 32
const int SDA_PIN = 21;
const int SCL_PIN = 22;

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Setup pins (if needed)
  for(int i=0; i<5; i++) {
    pinMode(FLEX_PINS[i], INPUT);
  }
}

void loop() {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // Basic Example: Using GET with query params or changes to POST
    // Construct data string (CSV format for simplicity or JSON)
    
    // Read sensors
    float flex[5];
    for(int i=0; i<5; i++) flex[i] = analogRead(FLEX_PINS[i]);
    
    // Placeholder for IMU (replace with actual simple MPU6050 read)
    float ax=0, ay=0, az=0, gx=0, gy=0, gz=0; 
    
    String payload = String(flex[0]) + "," + String(flex[1]) + "," + 
                     String(flex[2]) + "," + String(flex[3]) + "," + 
                     String(flex[4]) + "," + 
                     String(ax) + "," + String(ay) + "," + String(az) + "," + 
                     String(gx) + "," + String(gy) + "," + String(gz);
                     
    // Send data (Assuming backend accepts this via GET matching current serial format logic)
    // Or you can send JSON via POST
    
    // For now, let's just print to Serial for debugging
    // Serial.println(payload);
    
    // TODO: The backend currently expects SERIAL connection. 
    // To use Wi-Fi, the backend needs an HTTP endpoint to RECEIVE data.
    
    /* 
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST("{\"data\":\"" + payload + "\"}");
    http.end();
    */
  }
  
  delay(100); // 10Hz
}
