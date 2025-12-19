#ifndef CONFIG_H
#define CONFIG_H

// ---------------- Wi-Fi Configuration ----------------
// NOTE: DID NOT commit real credentials.
// Use placeholders and configure locally.

#define WIFI_SSID     "YOUR_WIFI_NAME"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// ---------------- Backend Configuration ----------------

// Local / LAN testing
#define SENSOR_POST_URL "http://YOUR_SERVER_IP:5000/sensor"

// ---------------- Timing Configuration ----------------

// Delay between sensor uploads (milliseconds)
#define SENSOR_POST_INTERVAL_MS 3000

#endif