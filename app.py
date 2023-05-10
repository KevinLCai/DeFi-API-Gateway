from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import csv
from database import Database
import logging
import datetime
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="env/.env")

PASSWORD = os.getenv('PASSWORD')

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["*"]}})
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'


def create_db_instance():
    db = Database(
        user='root',
        password=PASSWORD,
        host='localhost',
        database='defi_trading'
    )
    return db

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

def convert_data(data):
    asset = 'BTC'
    timestamp = datetime.datetime.strftime(data[3], '%Y-%m-%dT%H:%M:%S.%f')[:-3]
    price = float(data[1])
    size = float(data[6])
    direction = data[4]

    return {
        "asset": asset,
        "timestamp": timestamp,
        "price": price,
        "size": size,
        "direction": direction
    }


@app.route('/new_deal', methods=['POST'])
def new_deal():
    db = create_db_instance()
    is_invalid = db.is_not_valid()
    if is_invalid:
        return jsonify(is_invalid)

    recent_orders = db.get_recent_orders()
    db.close()

    # trade_data = {
    #                 "asset": "BTC",
    #                 "timestamp": "2023-05-10T12:34:56.789012",
    #                 "price": 45000.0,
    #                 "size": 0.5,
    #                 "direction": "buy"
    #             }
    trade_data = convert_data(recent_orders[0])
    print("RECENT ORDERS+=====")
    print(recent_orders)
    return jsonify(trade_data)

@app.route('/add_token', methods=['POST'])
def add_token():
    data = request.get_json()
    token_id = data.get('token_id')
    token_name = data.get('token_name')
    token_type = data.get('token_type')

    db = create_db_instance()
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

    # pw = input("Password: ")

    db = create_db_instance()
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

def new_deal_to_database(strategy, order_id, token_id, timestamp, order_type, order_price, order_size):

    db = create_db_instance()
    is_invalid = db.is_not_valid()
    if is_invalid:
        return jsonify(is_invalid)

    result = db.insert_deal(strategy, order_id, token_id, timestamp, order_type, order_price, order_size)
    db.close()

    if result:
        print("Successfully saved deal to database!")
        # send deal to frontend
        # message = {
        #     "timestamp": timestamp,
        #     "price": order_price,
        #     "size": order_size,
        #     "direction": order_type
        #     }
        # socketio.emit('cefi_deal', message)
        # print(f"Sent message: {message}")

        return jsonify({'status': 'success', 'message': 'Deal inserted successfully'})
    else:
        print("ERROR: Failed to store deal in database.")
        return jsonify({'status': 'error', 'message': 'Failed to insert deal'})

def get_token_ID(token):
    db = create_db_instance()
    is_invalid = db.is_not_valid()
    if is_invalid:
        return jsonify(is_invalid)

    result = db.get_token_id_by_name(token)
    db.close()

    return result

def new_deal_ID():
    db = create_db_instance()
    is_invalid = db.is_not_valid()
    if is_invalid:
        return jsonify(is_invalid)

    result = db.get_new_deal_id()
    db.close()
    return result

def cefi_deal(data):
    # get token id from token name
    try:
        token_id = get_token_ID(data['tokenID'])[0]
    except TypeError:
        token_id = None
    # create new dealID
    deal_id = new_deal_ID()

    if not token_id:
        logging.error(f"TokenID: {data['tokenID']} not found in Database")

    status = new_deal_to_database(data['strategy'], deal_id, token_id, datetime.datetime.fromtimestamp(data['timestamp']), data['orderType'], data['price'], data['size'])
    print(status)
 
@app.route("/deal", methods=["POST"])
def deal():
    print("New Trade")
    data = request.get_json()
    if data["strategy"] == "CeFi":
        cefi_deal(data)
    # Code to parse and save the data
    return "Data received and processed"

if __name__ == '__main__':
    app.run(debug=True)
