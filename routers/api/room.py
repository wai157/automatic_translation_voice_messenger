from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import current_user, login_required
from models import db, User, Room, ChatHistory
from datetime import datetime

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
                "room_name": room["room_id"].replace(f"{current_user.username}", "", 1).strip().replace("  ", " "),
                "last_message_timestamp": room["last_message_timestamp"].strftime('%a %d %b %Y, %I:%M%p')
            } for room in response]
        return response
    except Exception as e:
        print(e)
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
            room = Room.query.filter(Room.id == f"{current_user.username} {current_user.username}").first().serialize()
        else:
            rooms_current_user = User.query.filter(User.username == current_user.username).first().rooms
            print(rooms_current_user)
            rooms_user_to_find = User.query.filter(User.username == user_to_find.username).first().rooms
            print(rooms_user_to_find)
            matched_rooms = set(rooms_current_user).intersection(set(rooms_user_to_find))
            print(matched_rooms)
            if matched_rooms:
                matched_room = matched_rooms.pop()
                room = matched_room.serialize()
            else:
                new_room = Room(
                    id = f"{current_user.username} {user_to_find.username}"
                )
                db_current_user = User.query.filter(User.username == current_user.username).first()
                new_room.users.append(db_current_user)
                new_room.users.append(user_to_find)
                db.session.add(new_room)
                room = new_room.serialize()
                new_message = ChatHistory(
                    room_id = room["room_id"],
                    sender = "",
                    message = "Beginning of chat room",
                    timestamp = datetime.now()
                )
                db.session.add(new_message)
                new_room.messages.append(new_message)
                db.session.commit()
        messages = ChatHistory.query.filter(ChatHistory.room_id == room["room_id"]).all()
        messages = [message.serialize() for message in messages]
        return {
            "room_id": room["room_id"],
            "messages": messages
        }
    except Exception as e:
        db.session.rollback()
        print(e)
        return "An error occurred!", 500
