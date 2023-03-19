from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import csv
from database import Database
import logging


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

@app.route('/chart', methods=['POST'])
def chart():
    data = format_data('daily_BTC.csv')
    return jsonify(data)


# # @app.route('/add_token', methods=['POST'])
# # def add_token():
# pw = input("Password: ")
# db = Database(
#     user='root',
#     password=pw,
#     host='localhost',
#     database='defi_trading'
# )
# if db:
#     logging.info("MySQL Database Initialised")
# else:
#     logging.error("MySQL Database Failed to Load")


# db.insert_token(21, 'Bitcoin', 'Crypto')

# db.close()

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

    if db:
        logging.info("MySQL Database Initialised")
    else:
        logging.error("MySQL Database Failed to Load")

    result = db.insert_token(token_id, token_name, token_type)
    db.close()

    if result:
        return jsonify({'status': 'success', 'message': 'Token added successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to add token'})


if __name__ == '__main__':
    app.run(debug=True)
