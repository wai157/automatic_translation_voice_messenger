import logging.config
from flask import Blueprint, request
from flask_login import current_user, login_required
from models import db, User, Room, ChatHistory
import logging

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')

router = Blueprint('room', __name__, url_prefix='/rooms')

@router.route("/list", methods=["GET"], strict_slashes=False)
@login_required
def get_rooms():
    try:
        db_current_user = User.query.filter(User.username==current_user.username).first()
        rooms = Room.query.filter(Room.last_message_timestamp != None, Room.users.contains(db_current_user)).order_by(Room.last_message_timestamp.desc()).all()
        response = [room.serialize() for room in rooms]
        response = [
            {
                "room_id": room["room_id"],
                "room_name": room["room_id"].replace(f"{current_user.username}", "", 1).strip("-"),
                "last_message_timestamp": room["last_message_timestamp"]
            } for room in response]
        return response
    except Exception as e:
        logger.exception(e)
        return "An error occurred!", 500

@router.route("/find-room", methods=["GET"], strict_slashes=False)
@login_required
def find_room():
    try:
        user_to_find = request.args["user_to_find"]
        user_to_find = User.query.filter(User.username == user_to_find).first()
        if user_to_find is None:
            return "User not found!", 404
        if user_to_find.username == current_user.username:
            room = Room.query.filter(Room.id == f"{current_user.username}-{current_user.username}").first().serialize()
        else:
            rooms_current_user = User.query.filter(User.username == current_user.username).first().rooms
            rooms_user_to_find = User.query.filter(User.username == user_to_find.username).first().rooms
            matched_rooms = set(rooms_current_user).intersection(set(rooms_user_to_find))
            if matched_rooms:
                matched_room = matched_rooms.pop()
                room = matched_room.serialize()
            else:
                new_room = Room(
                    id = f"{current_user.username}-{user_to_find.username}"
                )
                db_current_user = User.query.filter(User.username == current_user.username).first()
                new_room.users.append(db_current_user)
                new_room.users.append(user_to_find)
                db.session.add(new_room)
                room = new_room.serialize()
                db.session.commit()
        messages = ChatHistory.query.filter(ChatHistory.room_id == room["room_id"]).order_by(ChatHistory.timestamp).all()
        messages = [message.serialize() for message in messages]
        return {
            "room_id": room["room_id"],
            "room_name": room["room_id"].replace(f"{current_user.username}", "", 1).strip("-"),
            "messages": messages
        }
    except Exception as e:
        db.session.rollback()
        logger.exception(e)
        return "An error occurred!", 500
