import os
from app.api.v1 import v1
from app.api.v2 import v2
from flask import Flask
from instance.config import DevelopmentConfig
from app.db_config import create_tables, drop_tables



def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)
    #drop_tables()
    create_tables(os.getenv('DB_URL'))
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    return app
