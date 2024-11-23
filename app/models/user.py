from app.utils.db import db

class User(db.Model):
    '''user model for storing account information'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

from app.utils.db import db
