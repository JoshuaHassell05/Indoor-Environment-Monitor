"""
Flask application to receive and serve sensor data.

Responsabilities:
- Accepts environmental sensor data via POST requests.
- Stores recent sensor data with timestamps.
- Serves as a web based dashboard for live monitoring.
"""
from flask import Flask, jsonify, request, render_template
from datetime import datetime

# --- Flask Application Setup ---
app = Flask(__name__)

# Memory data storage for recent sensor readings
data_store = []

# --- Web Routes ---
@app.route('/')
def index():
    # Render the main dashboard page
    return render_template('index.html')

# --- API Routes ---
@app.route('/data', methods=['POST'])
def sensor():
    # Receive sensor reading from ESP32 and store it with a timestamp
    data = request.get_json()
    if not data:
        return {'status': 'error', 'message': 'No data provided'}, 400
    data['timestamp'] = datetime.utcnow().isoformat()
    data_store.append(data)
    if len(data_store) > 200:
        data_store.pop(0)
    return {'status': 'success'}, 200

@app.route('/data', methods=['GET'])
def api_readings():
    # Return the stored sensor readings as JSON
    return jsonify(data_store)

# -- Application Entry Point ---
if __name__ == '__main__':
    # Devices on the local network can access the server
    app.run(host='0.0.0.0', port=5000, debug=True)
