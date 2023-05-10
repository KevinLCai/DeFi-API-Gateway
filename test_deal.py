import socketio

sio = socketio.Server()

@sio.on('connect')
def connect(sid, environ):
    print('connected', sid)

@sio.on('trigger_use_effect')
def trigger_use_effect(sid):
    print('Triggering useEffect')
    sio.emit('cefi_deal', {'timestamp': '2022-01-01 12:00:00', 'price': '100', 'size': '10', 'direction': 'buy'})

app = socketio.WSGIApp(sio)

import websocket

ws = websocket.WebSocket()
ws.connect('ws://127.0.0.1:5000/cefi_deal')
ws.send('trigger_use_effect')
