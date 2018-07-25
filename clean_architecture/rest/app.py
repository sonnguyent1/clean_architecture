from flask import Flask

from . import storage_room
from .settings import DevConfig


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(storage_room.blueprint)
    return app
