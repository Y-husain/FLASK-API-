from flask import Flask
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from app.configurations.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('configurations/config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from app.routes.auth import auth_blueprint
    # define the API resources
    app.register_blueprint(auth_blueprint)

    # add Rules for API Endpoints

    return app
