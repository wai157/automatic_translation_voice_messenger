import logging.config
from flask import Blueprint, request, current_app
from flask_socketio import send
from models import db, Room, ChatHistory
from datetime import datetime
import logging
import json
from gtts import gTTS

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')

router = Blueprint('rasp', __name__, url_prefix='/rasp')

@router.route("/", methods=["POST"], strict_slashes=False)
def log_from_rasp():
    key = request.headers["authorization"]
    if key != current_app.config["ADMIN_KEY"]:
        return "Unauthorized", 401
    
    try:
        room = "admin-admin"
        current_time = datetime.fromtimestamp(float(request.form['current_time']))
        sentences = json.loads(request.form['sentences'])
        original_text = sentences['original']
        translated_text = sentences['translated']
        original_voice = list(request.files['original'].read())
        tgt_lang = request.args.get("tgt_lang")
        audio = gTTS(text=translated_text, lang=tgt_lang, slow=False)
        audio.save(f"rasp.wav")
        with open(f"rasp.wav", "rb") as f:
            translated_voice = f.read()
        translated_voice = list(translated_voice)
        
        new_chat_history = ChatHistory(
            room_id = room,
            sender = "admin",
            original_voice = json.dumps(original_voice),
            original_text = original_text,
            translated_voice = json.dumps(translated_voice),
            translated_text = translated_text,
            timestamp = current_time
        )
        db.session.add(new_chat_history)
        chat_room: Room = Room.query.filter(Room.id == room).first()
        chat_room.last_message_timestamp = current_time
        request.namespace = '/'
        send(
            {
                "room_id": room,
                "room_name": "admin",
                "message": new_chat_history.serialize() 
            },
            to=room
        )
        db.session.commit()
        return "success", 200
    except Exception as e:
        logger.exception(e)
        db.session.rollback()
        return "An error occurred!", 500