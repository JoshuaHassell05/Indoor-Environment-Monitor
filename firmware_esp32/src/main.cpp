#include <Arduino.h>
#include <Wifi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>
const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASSWORD = "your_password";
const char* SENSOR_POST_URL = "http://YOUR_SERVER_IP:5000/sensor";
Adafruit_BME680 bme; // I2C
void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected");
  Serial.print("ESP32 IP address: ");
  Serial.println(WiFi.localIP());
}
bool initBME680() {
  if (bme.begin(0x77)) return true;
  if (bme.begin(0x76)) return true;
  return false;
}
void setup(){
    Serial.begin(115200);
    delay(500);
    Wire.begin();
    connectWiFi();
    if (!initBME680()) {
        Serial.println("BME680 not detected, Check wiring.");
        while(true) delay(1000);
    }
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    bme.setPressureOversampling(BME680_OS_4X);
    bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
    bme.setGasHeater(320, 150);
    Serial.println("BME680 initialized");
}
void loop(){
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("Wi-Fi disconnected, reconnecting...");
        connectWiFi();
    }
    if (!bme.performReading()) {
        Serial.println("Sensor reading failed");
        delay(3000);
        return;
    }
    float temperature = bme.temperature;
    float humidity = bme.humidity;
    float pressure = bme.pressure / 100.0;
    float gasResistance = bme.gas_resistance;
    String json =
        "{"
        "\"temperature\":" + String(temperature, 2) + ","
        "\"humidity\":" + String(humidity, 2) + ","
        "\"pressure\":" + String(pressure, 2) + ","
        "\"gas_resistance\":" + String(gasResistance, 2) +
        "}";
    Serial.println("Sending data: ");
    Serial.println(json);
    HTTPClient http;
    http.begin(SENSOR_POST_URL);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(json);
    Serial.print("HTTP Response code: ");
    Serial.printIn(httpCode)
    Serial.printIn(http.getString());
    http.end();
    delay(3000);
}
