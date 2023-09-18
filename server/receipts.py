import uuid
import os
from flask import Blueprint, request, render_template
from flask_login import login_required, current_user

from . import r2


receipts = Blueprint("receipts", __name__, template_folder="../templates", static_folder="../static")


@receipts.route("/addreceipt", methods=["GET", "POST"])
@login_required
def addreceipt():
    if request.method == "POST":
        receipt_id = str(uuid.uuid4())
        company = request.form.get("company")
        item_name = request.form.get("item-name")
        purchase_data = request.form.get("purchase-date")
        price = request.form.get("price")
        receipt = request.files.get("receipt")

        print(os.path.join(f"tmp/{receipt_id}.{receipt.filename.split('.')[1]}"))
        receipt.save(os.path.join(f"tmp/{receipt_id}.{receipt.filename.split('.')[1]}"))
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
