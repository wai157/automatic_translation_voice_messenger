from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config


migrate = Migrate()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    return app