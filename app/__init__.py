from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config_options
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet,configure_uploads,IMAGES
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_mail import Mail

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


bootstrap=Bootstrap()
db = SQLAlchemy()
mail = Mail()

photos = UploadSet('photos',IMAGES)
def create_app(config_name):
    #Initializing application
    app = Flask(__name__)

    # Create the app configuration
    app.config.from_object(config_options[config_name])

    # configure UploadSet
    configure_uploads(app,photos)

    # Initializing flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    mail.init_app(app)


    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/auth')


    # setting config
    # from .requests import configure_request
    # configure_request(app)

    # Will add the views and forms

    return app 