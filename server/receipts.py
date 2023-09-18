from flask import Blueprint, request, render_template
from flask_login import login_required, current_user


receipts = Blueprint("receipts", __name__, template_folder="../templates", static_folder="../static")


@receipts.route("/addreceipt", methods=["GET", "POST"])
@login_required
def addreceipt():
    if request.method == "POST":
        return "", 200
    else:
        return render_template("addreceipt.html")
