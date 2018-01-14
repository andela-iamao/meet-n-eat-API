from flask import Flask
from flask_mongoengine import MongoEngine
from user.views import user_app

from flask_jwt_extended import JWTManager

db = MongoEngine()


def create_app(**config_overrides):
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')
    app.config.update(config_overrides)

    db.init_app(app)

    app.register_blueprint(user_app, url_prefix="/api/v1/user")

    JWTManager(app)

    return app
