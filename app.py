from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello', methods=['POST'])
def hello():
    name = request.json.get('name', '')
    message = f"Hello, {name}!"
    return jsonify({'message': message})