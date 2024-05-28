from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }
            

class Room(db.Model):
    __tablename__ = "room"
    
    id = db.Column(db.Integer, autoincrement=True)
    first_user = db.Column(db.String(16), db.ForeignKey("user.username"), primary_key=True, nullable=False)
    second_user = db.Column(db.String(16), db.ForeignKey("user.username"), primary_key=True, nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "first_user": self.first_user,
            "second_user": self.second_user,
        }
    

class ChatHistory(db.Model):
    __tablename__ = "chat_history"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    sender = db.Column(db.String(16), db.ForeignKey("user.username"), nullable=False)
    message = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "sender": self.sender,
            "message": self.message,
            "timestamp": self.timestamp,
        }
    