from flask import Flask
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from app.configurations.config import app_config
from app.handlers.error_handler import JsonExceptionHandler

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('configurations/config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from app.routes.auth import auth_blueprint
    from app.routes.categories import category_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(category_blueprint)
    JsonExceptionHandler(app)

    return app
