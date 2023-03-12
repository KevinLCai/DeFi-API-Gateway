from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from Flask!'})


# @app.route('/pnl', methods=['POST'])
# def pnl():
#     name = request.json.get('name', '')
#     message = f"{name}"
#     return jsonify({'message': message})


@app.route('/candlestick')
def get_candlestick_data():
    # Load candlestick data from a CSV file or database
    # For example:
    df = pd.read_csv('daily_BTC.csv')

    # Convert the data to a list of dictionaries
    data = df.to_dict(orient='records')

    return jsonify(data)
