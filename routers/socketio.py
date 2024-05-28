from flask_socketio import SocketIO, join_room, leave_room, send
from flask_login import current_user

socketio = SocketIO()

@socketio.on("connect")
def connect():
    print("connected")

@socketio.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)
    print(current_user.username + " has entered room " + room)
    send(current_user.username + " has entered room " + room, to=room)
    
@socketio.on("leave")
def on_leave(data):
    room = data["room"]
    leave_room(room)
    print(current_user.username + " has left room " + room)
    send(current_user.username + " has left room " + room, to=room)