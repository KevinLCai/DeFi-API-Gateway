from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import csv
from database import Database
import logging
from flask_socketio import SocketIO, emit, send
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins='*')

@app.route('/')
def hello_world():
    return 'Hello, World!'


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


@app.route('/add_token', methods=['POST'])
def add_token():
    data = request.get_json()
    token_id = data.get('token_id')
    token_name = data.get('token_name')
    token_type = data.get('token_type')

    pw = input("Password: ")
    db = Database(
        user='root',
        password=pw,
        host='localhost',
        database='defi_trading'
    )
    is_invalid = db.is_not_valid()
    if is_invalid:
        return jsonify(is_invalid)

    result = db.insert_token(token_id, token_name, token_type)
    db.close()

    if result:
        return jsonify({'status': 'success', 'message': 'Token added successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to add token'})


@app.route('/get_token', methods=['GET'])
def get_token():
    token_id = request.args.get('token_id')

    pw = input("Password: ")

    db = Database(
        user='root',
        password=pw,
        host='localhost',
        database='defi_trading'
    )
    is_invalid = db.is_not_valid()
    if is_invalid:
        return jsonify(is_invalid)

    result = db.get_token_by_id(token_id)
    db.close()

    if result:
        return jsonify({'status': 'success', 'data': result})
    else:
        return jsonify({'status': 'error', 'message': 'Token not found'})


# CeFi Endpoints:

@app.route("/cefi_historical", methods=["POST"])
def cefi_historical():
    data = request.get_json()
    print(data)
    # Code to parse and save the data
    return "Data received and processed"


def format_trade_data(trade_data):
    formatted_data = {}
    formatted_data['timestamp'] = trade_data['timestamp']
    formatted_data['price'] = trade_data['price']
    formatted_data['size'] = trade_data['size']
    formatted_data['direction'] = trade_data['direction'].lower()
    return json.dumps(formatted_data)

@socketio.on('cefi_deal', namespace='/cefi_deal')
def cefi_deal(data):
    data_to_send = format_trade_data(data)
    print(data_to_send)
    socketio.send(data_to_send, namespace='/cefi_deal')
    # socketio.emit('cefi_deal', data_to_send)
    print("EMITTED")
 

@app.route("/deal", methods=["POST"])
def deal():
    data = request.get_json()
    strategy = data["strategy"]
    del data["strategy"]
    if strategy == "CeFi":
        # cefi_deal(data)
        data = {'message': 'Hello from Flask!'}
        socketio.emit('data', data)
        return jsonify(data)

    elif strategy == "Flashloan":
        pass
    elif strategy == "YieldFarm":
        pass

    # Code to parse and save the data
    return "Data received and processed"

if __name__ == '__main__':
    socketio.run(app, debug=True)
