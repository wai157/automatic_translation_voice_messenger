from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    username = db.Column(db.String(16), primary_key=True)
    pwd = db.Column(db.String(), primary_key=False)