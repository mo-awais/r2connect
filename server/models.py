from . import db


class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
