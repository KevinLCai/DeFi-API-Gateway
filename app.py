from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import csv
from database import Database
import logging
import datetime


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


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

def new_deal_to_database(strategy, order_id, token_id, timestamp, order_type, order_price, order_size):
 
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

    result = db.insert_deal(strategy, order_id, token_id, timestamp, order_type, order_price, order_size)
    db.close()

    if result:
        return jsonify({'status': 'success', 'message': 'Deal inserted successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to insert deal'})

def get_token_ID(token):
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

    result = db.get_token_id_by_name(token)
    db.close()

    return result

def cefi_deal(data):
    # get token id from token name
    token_id = get_token_ID(data['tokenID'])[0]

    if not token_id:
        logging.error(f"TokenID: {data['tokenID']} not found in Database")
    print("TOKEN_ID===========")
    print(token_id)

    status = new_deal_to_database(data['strategy'], data['dealID'], token_id, datetime.datetime.fromtimestamp(data['timestamp']), data['orderType'], data['price'], data['size'])
    print(status)

@app.route("/deal", methods=["POST"])
def deal():
    data = request.get_json()
    if data["strategy"] == "CeFi":
        cefi_deal(data)
    # Code to parse and save the data
    return "Data received and processed"

if __name__ == '__main__':
    app.run(debug=True)
