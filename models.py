from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

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
            "last_message_timestamp": self.last_message_timestamp,
        }
    

class ChatHistory(db.Model):
    __tablename__ = "chat_history"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.String(36), db.ForeignKey("room.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    sender = db.Column(db.String(16), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    message = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    
    def serialize(self):
        return {
            "room_id": self.room_id,
            "sender": self.sender,
            "message": self.message,
            "timestamp": self.timestamp,
        }
    