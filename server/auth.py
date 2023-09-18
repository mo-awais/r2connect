import uuid
from flask import Blueprint, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db, r2
from exceptions.cloudflare.r2 import BucketAlreadyExists


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("index.home"))
    else:
        return "", 200


@auth.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user:
        return "This user already exists", 400

    user_id = str(uuid.uuid4())
    new_user = User(id=user_id, username=username, password=generate_password_hash(password, method="scrypt"))

    try:
        r2.create_bucket(user_id)

        db.session.add(new_user)
        db.session.commit()

        return f"Successfully created an account for {username} with id {user_id}", 200
    except BucketAlreadyExists:
        return f"Failed to create a bucket for the following user {username}", 500
