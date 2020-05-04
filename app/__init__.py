from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config_options


db = SQLAlchemy()


def create_app(config_name):
    #Initializing application
    app = Flask(__name__)

    # Create the app configuration
    app.config.from_object(config_options[config_name])

    # Initializing flask extensions
    db.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # setting config
    # from .requests import configure_request
    # configure_request(app)

    # Will add the views and forms

    return app 