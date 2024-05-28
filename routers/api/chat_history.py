from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_required
from models import db, User, Room, ChatHistory
from sqlalchemy import or_

router = Blueprint('chat_history', __name__, url_prefix='/chat-history')

@router.route("/rooms", methods=["GET"], strict_slashes=False)
@login_required
def get_rooms():
    rooms = Room.query.filter(or_(Room.first_user == current_user.username, Room.second_user == current_user.username)).all()
    response = [room.serialize() for room in rooms]
        
    return response