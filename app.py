from flask_login import current_user

from karaoke_online_hakaton import create_app
from flask import url_for
from flask_security import roles_required
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from DataBase import User


app = create_app(debug=True)


socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('join_room')
def on_connect(data):
    user = User.objects(id=current_user.id)[0]
    username = data["username"]
    room = data["roomid"]
    join_room(room)
    emit('chatmessage_get', {'msg': username + ' has entered the room.', 'username': 'System'}, room=room)

@socketio.on('leave')
def on_leave(roomid):
    user = User.objects(id=current_user.id)[0]
    username = roomid
    room = (roomid + user.username)
    leave_room(room)
    send(username + ' has left the room.', to=room)

@socketio.on('chatmessage')
def handle_message(data):
    username = data["username"]
    print('Message: ' + data['msg'], data['roomid'])
    emit('chatmessage_get', {'username':username ,'msg': data['msg']} ,room=data['roomid'])



@app.before_first_request
def restrict_admin_url():
    endpoint = "admin.index"
    url = url_for(endpoint)
    admin_index = app.view_functions.pop(endpoint)

    @app.route(url, endpoint=endpoint)
    @roles_required('admin')
    def secure_admin_index():
        return admin_index()

if __name__ == "__main__":
    socketio.run(app)
