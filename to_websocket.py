from flask import Flask
from flask_socketio import SocketIO, emit
import random
import time
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
socketio = SocketIO(app)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/emit_trade')
def emit_trade():
    trade_data = {
        "Timestamp": str(time.time()),
        "Price": random.uniform(40000, 50000),
        "Size": random.uniform(0.1, 1.0),
        "Direction": random.choice(["buy", "sell"])
    }
    print("EMITTING DATA===========")
    print(trade_data)
    socketio.emit('cefi_deal', trade_data)
    return 'OK'

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=3001)
