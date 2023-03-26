from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)

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
    data = request.get_json()
    print("DATA=======")
    print(data)
    data = {'message': 'Hello from the backend!'}
    send_data(data)

    return jsonify({'success': True})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
