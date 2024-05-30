from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_login import current_user
from models import db, ChatHistory, Room
import requests
from gtts import gTTS
import os
import subprocess
from datetime import datetime
import json

socketio = SocketIO()

@socketio.on("connect")
def on_connect():
    join_room(current_user.username)
    print("connected")
    
@socketio.on("disconnect")
def on_disconnect():
    print("disconnected")

@socketio.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)
    print(current_user.username + " has entered room " + room)
    
@socketio.on("leave")
def on_leave(data):
    room = data["room"]
    leave_room(room)
    print(current_user.username + " has left room " + room)
    
@socketio.on("audio")
def on_audio(data):
    try:
        current_time = datetime.now()
        room = data["room"]
        user_to_send = room.replace(f"{current_user.username}", "", 1).strip("-")
        original_voice = data["audio"]
        tgt_lang = data["tgt_lang"]
        src_lang = data["src_lang"]
        filename = os.urandom(8).hex()
        with open(f"{filename}.webm", "wb") as f:
            f.write(original_voice)
        subprocess.call([
            'ffmpeg',
            '-i', f"{filename}.webm", f"{filename}.wav",
        ])
        with open(f"{filename}.wav", "rb") as f:
            original_voice = f.read()
        original_voice = list(original_voice)
        url = "http://127.0.0.1:8080"
        response = requests.post(
            url,
            files={'file': open(f"{filename}.wav", 'rb')},
            params={"lang": src_lang},
            timeout=15
        )
        if response.status_code == 200:
            original_text = response.json()['original_text']
            translated_text = response.json()['translated_text']
        else:
            raise Exception("Failed to get response from the server")
        audio = gTTS(text=translated_text, lang=tgt_lang, slow=False)
        audio.save(f"resp_{filename}.wav")
        with open(f"resp_{filename}.wav", "rb") as f:
            translated_voice = f.read()
        translated_voice = list(translated_voice)
        new_chat_history = ChatHistory(
            room_id = room,
            sender = current_user.username,
            original_voice = json.dumps(original_voice),
            original_text = original_text,
            translated_voice = json.dumps(translated_voice),
            translated_text = translated_text,
            timestamp = current_time
        )
        db.session.add(new_chat_history)
        chat_room = Room.query.filter(Room.id == room).first()
        chat_room.last_message_timestamp = current_time
        os.remove(f"{filename}.webm")
        os.remove(f"{filename}.wav")
        os.remove(f"resp_{filename}.wav")
        send(
            {
                "room_id": room,
                "room_name": user_to_send,
                "message": new_chat_history.serialize() 
            },
            to=room
        )
        emit(
            "new_msg",
            {
                "room_id": room,
                "room_name": current_user.username,
                "last_message_timestamp": current_time.strftime('%a %d %b %Y, %I:%M%p'),
            },
            to=user_to_send
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        if os.path.exists(f"{filename}.webm"):
            os.remove(f"{filename}.webm")
        if os.path.exists(f"{filename}.wav"):
            os.remove(f"{filename}.wav")
        if os.path.exists(f"resp_{filename}.webm"):
            os.remove(f"resp_{filename}.wav")
        emit("error")