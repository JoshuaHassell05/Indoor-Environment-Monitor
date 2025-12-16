#include <Arduino.h>
#include <Wifi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>
const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASSWORD = "your_password";
const char* SENSOR_POST_URL = "http://YOUR_SERVER_IP:5000/sensor";

