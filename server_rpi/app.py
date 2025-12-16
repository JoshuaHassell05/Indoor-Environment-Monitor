"""
Flask application to receive and serve sensor data.

Responsibilities:
- Accepts environmental sensor data via POST requests.
- Stores recent sensor data with timestamps.
- Serves as a web based dashboard for live monitoring.
"""
from analytics import attach_risk_fields
from flask import Flask, jsonify, request, render_template
from datetime import datetime
from db import init_db, insert_reading, fetch_recent_readings

# --- Flask Application Setup ---
app = Flask(__name__)
init_db()

# Memory data storage for recent sensor readings
READINGS = []

# --- Web Routes ---
@app.route('/')
def index():
    # Render the main dashboard page
    return render_template('index.html')

# --- API Routes ---
@app.route('/sensor', methods=['POST'])
def sensor():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    data['timestamp'] = datetime.utcnow().isoformat()
    data = attach_risk_fields(data)
    READINGS.append(data)
    if len(READINGS) > 100:
        READINGS.pop(0)
    return jsonify({'status': 'success'}), 200

@app.route('/api/readings', methods=['GET'])
def api_readings():
    # Return the stored sensor readings as JSON
    return jsonify(READINGS)

# -- Application Entry Point ---
if __name__ == '__main__':
    # Devices on the local network can access the server
    app.run(host='0.0.0.0', port=5000, debug=True)
