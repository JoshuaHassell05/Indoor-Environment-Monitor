# Indoor-Environment-Monitor
Real-time IoT environmental safety monitoring using ESP32 + Raspberry Pi, with live dashboard and hazard analysis.
## 🚧 Project Status: In Development
This repository currently contains the initial project structure, planned features, and setup details.  
Firmware, server code, dashboard, and documentation will be added progressively as the project is built.

---
## Goal of the Project
The purpose of this project is to create a small, portable device capable of monitoring indoor environmental health indicators such as temperature, humidity, pressure, and VOC-based air quality.

Data will be transmitted from an ESP32 to a Raspberry Pi, which will host a web dashboard for real-time viewing.

This project demonstrates:
- Embedded firmware development  
- Sensor communication (I2C)  
- Wireless networking (Wi-Fi, HTTP)  
- Backend API development (Flask)  
- Real-time dashboard design  

---

## Planned Features
- Read environmental data from a **BME680 sensor**
- ESP32 sends JSON packets to Raspberry Pi server
- Flask backend receives, stores, and processes sensor data
- Web dashboard displays:
  - Temperature  
  - Humidity  
  - Pressure  
  - Gas resistance / VOC indicator
- Basic risk evaluation (SAFE / ELEVATED / WARNING)
- Modular architecture easy to expand
  
---

## Hardware List
- ESP32 Dev Board (ESP-WROOM-32)
- BME680 Environmental Sensor
- Raspberry Pi (Pi 4 or Pi Zero 2 W)
- Breadboard + jumper wires
- USB cables for power/programming

More hardware may be added later as features expand.

---
## Project Status: In Development
This repository currently contains the initial project structure, planned features, and setup details.  
Firmware, server code, dashboard, and documentation will be added progressively as the project is built.

---

## Goal of the Project
The purpose of this project is to create a small, portable device capable of monitoring indoor environmental health indicators such as temperature, humidity, pressure, and VOC-based air quality.

Data will be transmitted from an ESP32 to a Raspberry Pi, which will host a web dashboard for real-time viewing.

This project demonstrates:
- Embedded firmware development  
- Sensor communication (I2C)  
- Wireless networking (Wi-Fi, HTTP)  
- Backend API development (Flask)  
- Real-time dashboard design  

---

## 🛠 Planned Features
- Read environmental data from a **BME680 sensor**
- ESP32 sends JSON packets to Raspberry Pi server
- Flask backend receives, stores, and processes sensor data
- Web dashboard displays:
  - Temperature  
  - Humidity  
  - Pressure  
  - Gas resistance / VOC indicator
- Basic risk evaluation (SAFE / ELEVATED / WARNING)
- Modular architecture easy to expand

**Future planned upgrades:**
- Historical charts  
- Additional sensors (CO₂, noise, light)  
- Local OLED display  
- Data logging (SQLite or InfluxDB)  
- Cloud deployment  

---

## 🔌 Hardware List
- ESP32 Dev Board (ESP-WROOM-32)
- BME680 Environmental Sensor
- Raspberry Pi (Pi 4 or Pi Zero 2 W)
- Breadboard + jumper wires
- USB cables for power/programming

More hardware may be added later as features expand.

---

## Setup (Coming Soon)
Instructions for setting up the ESP32 firmware and Raspberry Pi server will be added once the initial prototypes are running.

---

## Screenshots (Coming Soon)
Images of the wiring, dashboard UI, and system output will be included as the project develops.

---

## License
MIT License

---

## Author
**Joshua Hassell**  
Computer Engineering Student  
University of Kansas  

---
