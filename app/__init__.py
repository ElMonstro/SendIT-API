import os
from app.api.v1 import v1
from app.api.v2 import v2
from flask import Flask
from config import config_dict
from .db_config import DbConnect


def create_app(config='dev'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config])
    db_conn = DbConnect(config)
    db_conn.create_tables()
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    return app
