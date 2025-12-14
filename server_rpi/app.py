from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)
data_store = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def sensor():
    data = request.get_json()
    if not data:
        return {'status': 'error', 'message': 'No data provided'}, 400
    data['timestamp'] = datetime.utcnow().isoformat()
    data_store.append(data)
    if len(data_store) > 200:
        data_store.pop(0)
    return {'status': 'success'}, 200
