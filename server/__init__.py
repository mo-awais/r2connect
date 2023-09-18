import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import Config
from utils.cloudflare.r2 import R2


db = SQLAlchemy()
r2 = R2()


def create_app():
    Config()

    server = Flask(__name__, template_folder="templates", static_folder="static")

    server.config["SECRET_KEY"] = os.environ.get("SQLALCHEMY_SECRET_KEY")
    server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    db.init_app(server)

    login_manager = LoginManager()
    login_manager.login_view = "index.home"
    login_manager.init_app(server)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from .auth import auth as auth_blueprint
    server.register_blueprint(auth_blueprint)

    from .index import index as index_blueprint
    server.register_blueprint(index_blueprint)

    return server
