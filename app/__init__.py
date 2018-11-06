from app.api.v1 import v1
from flask import Flask
from instance.config import DevelopmentConfig


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)
    app.register_blueprint(v1)
    return app


