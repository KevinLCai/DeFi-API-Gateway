from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from database import Database
from dotenv import load_dotenv
import os
import csv

load_dotenv(dotenv_path="env/.env")

PASSWORD = os.getenv('PASSWORD')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)

def create_db_instance():
    db = Database(
        user='root',
        password=PASSWORD,
        host='localhost',
        database='defi_trading'
    )
    return db

def format_data(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header row
        for row in reader:
            date = row[0]
            close_price = float(row[4])
            obj = {'time': date, 'value': int(close_price)}
            data.append(obj)
    return data

# Frontend Endpoints: 

@app.route('/chart', methods=['POST'])
def chart():
    data = format_data('daily_BTC.csv')
    return jsonify(data)

@socketio.on('connect')
def test_connect():
    print('Client connected')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    
def send_data(data):
    socketio.emit('data_from_backend', {'data': data}, include_self=True)

@app.route("/deal", methods=["POST"])
def deal():
    print("DEAL")
    data = request.get_json()
    print("DATA=======")
    print(data)
    # data = {'message': 'Hello from the backend!'}
    data.pop('fees', None)
    send_data(data)

    return jsonify({'success': True})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
