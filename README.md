# Indoor-Environment-Monitor
An end-to-end IoT indoor environmental monitoring system using an ESP32 & BME680 with both a local Flask backend and a cloud AWS backend for live web dashboard.

## Project Status: Completed
This project is fully implemented and operational. The ESP32 collects sensor data, transmits it to either a local or cloud backend, stores readings, evaluates risk levels, and displays live data on the dashboard.

---

## Live Demo
http://indoor-env-monitor-dashboard-265781770234.s3-website-us-east-1.amazonaws.com
> Hosted using Amazon S3 static website hosting (HTTP).
---

## Goal of the Project
Build a device capable of monitoring indoor environmental health indicators such as:
- Temperature
- Humidity
- Pressure
- Gas resistance (VOC / air quality proxy)

This project demonstrates:
- Embedded firmware development (ESP32)
- Sensor communication (I2C)
- Wireless networking (Wi-Fi, HTTP/HTTPS)
- Backend API development (Flask + AWS Lambda)
- Cloud deployment (API Gateway, DynamoDB, S3)
- Real-time dashboard design

---

## Implemented Features
- Reads environmental data from a BME680 sensor over I2C
- ESP32 sends JSON packets to:
  - Local Flask server (HTTP), or
  - AWS API Gateway (HTTPS)
- Backends receive, store, and serve readings via REST APIs
- Web dashboard displays:
  - Temperature
  - Humidity
  - Pressure
  - Gas resistance / VOC indicator
- Risk evaluation states:
  - SAFE
  - ELEVATED
  - WARNING
- Historical charts with time-bucketed averages (day / week / month)

---

## Setup Overview
- Firmware: Configure Wi-Fi locally and choose local vs cloud target using headers in `firmware_esp32/include/`
- Local backend: Run Flask from `server_rpi/`
- Cloud backend: Deploy serverless stack from `cloud_aws/` using AWS SAM
- Dashboard: Serve locally (Flask) or upload to S3 for cloud hosting

---

## Hardware List
- ESP32 Dev Board (ESP-WROOM-32)
- BME680 Environmental Sensor
- Breadboard + jumper wires
- USB cables for power/programming

---

## License
MIT License

---

## Author
Joshua Hassell  
Computer Engineering Student  
University of Kansas
