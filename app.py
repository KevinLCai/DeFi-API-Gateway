from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/data', methods=['POST'])
def get_data():
    data = request.get_json()
    name = data['data']
    message = f"Hello, {name}!"
    return jsonify({'message': message})


@app.route('/chart', methods=['POST'])
def chart():
    data = [
        {'time': '2022-01-01', 'value': 100},
        {'time': '2022-01-02', 'value': 110},
        {'time': '2022-01-03', 'value': 105},
        {'time': '2022-01-04', 'value': 115},
        {'time': '2022-01-05', 'value': 120},
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
