from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)
data_store = []

@app.route('/')
def index():
    return render_template('index.html')
