#include <Arduino.h>
#include <Wifi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>
/*
    ESP32 Firmware to read BME680 sensor data and send it to a server via HTTP POST.
*/

// Wi-Fi credentials: Place holder values here
const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASSWORD = "your_password";
const char* SENSOR_POST_URL = "http://YOUR_SERVER_IP:5000/sensor";

Adafruit_BME680 bme; // I2C instance

// Establish Wi-Fi connection
void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected");
  Serial.print("ESP32 IP address: ");
  Serial.println(WiFi.localIP());
}

// Initialize BME680 sensor
bool initBME680() {
  if (bme.begin(0x77)) return true;
  if (bme.begin(0x76)) return true;
  return false;
}

// Main setup 
void setup(){
    Serial.begin(115200);
    delay(500);
    Wire.begin();
    connectWiFi();
    if (!initBME680()) {
        // Halt if sensor not found
        Serial.println("BME680 not detected, Check wiring.");
        while(true) delay(1000);
    }
    // Sensor configuration prioritizing accuracy over speed
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    bme.setPressureOversampling(BME680_OS_4X);
    // Smoothing filter
    bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
    // Enable gas sensor with heater profile
    bme.setGasHeater(320, 150);
    Serial.println("BME680 initialized");
}

// Main loop to read sensor and send data
void loop(){
    // Ensure Wi-Fi is connected
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("Wi-Fi disconnected, reconnecting...");
        connectWiFi();
    }
    // Read sensor data
    if (!bme.performReading()) {
        Serial.println("Sensor reading failed");
        delay(3000);
        return;
    }
    // Acquire sensor values
    float temperature = bme.temperature;
    float humidity = bme.humidity;
    float pressure = bme.pressure / 100.0;
    float gasResistance = bme.gas_resistance;
    // Prepare JSON payload
    String json =
        "{"
        "\"temperature\":" + String(temperature, 2) + ","
        "\"humidity\":" + String(humidity, 2) + ","
        "\"pressure\":" + String(pressure, 2) + ","
        "\"gas_resistance\":" + String(gasResistance, 2) +
        "}";
    // Send data via HTTP POST
    Serial.println("Sending data: ");
    Serial.println(json);
    HTTPClient http;
    http.begin(SENSOR_POST_URL);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(json);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    Serial.println(http.getString());
    http.end();
    // Transmission interval
    delay(3000);
}

