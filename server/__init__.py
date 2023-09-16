import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv


load_dotenv("test.env")
db = SQLAlchemy()


def create_app():
    server = Flask(__name__, template_folder="templates", static_folder="static")

    server.config["SECRET_KEY"] = os.environ.get("SQLALCHEMY_SECRET_KEY")
    server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    db.init_app(server)

    from .auth import auth as auth_blueprint
    server.register_blueprint(auth_blueprint)

    from .index import index as index_blueprint
    server.register_blueprint(index_blueprint)

    return server
