from flask import Blueprint
from . import db


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    return '', 200
