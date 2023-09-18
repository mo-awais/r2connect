from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Receipts(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    company = db.Column(db.String(100))
    item_name = db.Column(db.String(100))
    purchase_date = db.Column(db.String(100))
    price = db.Column(db.String(100))
