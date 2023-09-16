from flask import Blueprint, send_from_directory, render_template
from . import db


index = Blueprint("index", __name__, template_folder="../templates", static_folder="../static")


@index.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory("static/images", "favicon.ico")


@index.route("/", methods=["GET"])
def home():
    return render_template("index.html")
