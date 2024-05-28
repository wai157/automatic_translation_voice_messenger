from flask_socketio import SocketIO, join_room, leave_room, send
from flask_login import current_user
import requests
from gtts import gTTS
import os

socketio = SocketIO()

@socketio.on("connect")
def on_connect():
    print("connected")
    
@socketio.on("disconnect")
def on_disconnect():
    print("disconnected")

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
    
@socketio.on("audio")
def on_audio(data):
    room = data["room"]
    audio = data["audio"]
    tgt_lang = data["tgt_lang"]
    src_lang = data["src_lang"]
    print(audio)
    filename = os.urandom(16).hex()
    with open(f"{filename}.wav", "wb") as f:
        f.write(audio)
    url = "http://127.0.0.1:8080"
    response = requests.post(
        url,
        files={'file': open(f"{filename}.wav", 'rb')},
        params={"lang": src_lang},
        timeout=15
    )
    # if os.path.exists(filename):
    # 	os.remove(filename)
    print(response.text)
    if response.status_code == 200:
        text = response.json()['text']
        print(text)
    #     audio = gTTS(text=text, lang=tgt_lang, slow=False)
    #     audio.save("audio.wav")
    #     print("Playing audio...")
    #     print("Audio ended")
    # else:
    #     print("Error")