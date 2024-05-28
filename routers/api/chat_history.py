from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import current_user, login_required
from models import db, User, Room, ChatHistory
from sqlalchemy import or_

router = Blueprint('chat_history', __name__, url_prefix='/chat-history')

@router.route("/get", methods=["GET"], strict_slashes=False)
@login_required
def get_chat_history():
    room_id = request.args["room_id"]
    chat_history = ChatHistory.query.filter(ChatHistory.room_id == room_id).order_by(ChatHistory.timestamp.desc()).all()
    response = [message.serialize() for message in chat_history]

    return response