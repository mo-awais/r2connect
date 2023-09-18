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


@receipts.route("/viewreceipts", methods=["GET"])
@login_required
def viewreceipts():
    receipts1 = [
        {
            "id": "12345",
            "company": "Apple",
            "item_name": "Apple TV 4K",
            "price": "169.00",
            "purchase_date": "14-09-2023"
        }
    ]
    return render_template("viewreceipts.html", receipts=receipts1)
