import sqlite3
from db import db


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone_number = db.Column(db.String(80))

    def __init__(self, username, password, name, email, phone_number):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def json(self):
        return {
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).all()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
