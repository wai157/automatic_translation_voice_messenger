from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

room_user = db.Table("room_user",
    db.Column('room_id', db.String(36), db.ForeignKey("room.id", onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('username', db.String(16), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE")),              
)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    rooms = db.relationship("Room", secondary=room_user, back_populates="users")
    
    def serialize(self):
        return {
            "username": self.username,
        }
            

class Room(db.Model):
    __tablename__ = "room"
    
    id = db.Column(db.String(36), primary_key=True)
    last_message_timestamp = db.Column(db.DateTime(), nullable=True)

    users = db.relationship("User", secondary=room_user, back_populates="rooms")
    messages = db.relationship("ChatHistory", backref="room")

    def serialize(self):
        return {
            "room_id": self.id,
            "last_message_timestamp": self.last_message_timestamp.strftime('%a %d %b %Y, %I:%M%p') if self.last_message_timestamp else None,
        }
    

class ChatHistory(db.Model):
    __tablename__ = "chat_history"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.String(36), db.ForeignKey("room.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    sender = db.Column(db.String(16), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    original_voice = db.Column(db.String())
    original_text = db.Column(db.String())
    translated_voice = db.Column(db.String())
    translated_text = db.Column(db.String())
    timestamp = db.Column(db.DateTime())
    
    def serialize(self):
        return {
            "room_id": self.room_id,
            "sender": self.sender,
            "original_voice": json.loads(self.original_voice),
            "original_text": self.original_text,
            "translated_voice": json.loads(self.translated_voice),
            "translated_text": self.translated_text,
            "timestamp": self.timestamp.strftime('%a %d %b %Y, %I:%M%p'),
        }
    