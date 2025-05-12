from app import db 
from datetime import datetime


class User(db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    date = db.Column(db.String(30), default=datetime.now().date())
    address = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Integer)
    booking_info = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"<Username {self.username}>"
    