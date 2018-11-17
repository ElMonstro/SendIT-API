import os
from app.api.v1 import v1
from app.api.v2 import v2
from flask import Flask
from config import config_dict
from app.db_config import create_tables, drop_tables



def create_app(config='dev'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_dict[config])
    #drop_tables()
    create_tables(config_dict[config].DB_URL)
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    return app
