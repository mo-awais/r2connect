from flask import Blueprint, send_from_directory, render_template, redirect, url_for
from flask_login import login_required, current_user


index = Blueprint("index", __name__, template_folder="../templates", static_folder="../static")


@index.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory("static/images", "favicon.ico")


@index.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("index.dashboard"))
    else:
        return render_template("index.html")


@index.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)
