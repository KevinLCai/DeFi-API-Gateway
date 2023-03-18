from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import csv

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


# @app.route('/chart', methods=['POST'])
# def chart():
#     data = []

#     df = pd.read_csv('daily_BTC.csv')
#     first_row = df.iloc[0]

#     counter = 0
#     for index, row in df.iterrows():
#         new_row = {
#             'time': row['Date'],
#             'value': row['Open']
#         }
#         # print(new_row)
#         if counter<4:
#             print(new_row)
#             data.append(new_row)
#             counter += 1


#     data.append({'time': '2022-01-05', 'value': 120},)

#     return jsonify(data)

import csv

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

if __name__ == '__main__':
    app.run(debug=True)
