from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from models import db
    from routers.authentication import login_manager, bcrypt
    
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    from routers import authentication
    from routers import home
    from routers.api import chat_history
    
    app.register_blueprint(authentication.router)
    app.register_blueprint(home.router)
    app.register_blueprint(chat_history.router)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)