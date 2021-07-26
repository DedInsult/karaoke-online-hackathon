from app import socketio, send



@socketio.on('message')
def handle_message(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)
