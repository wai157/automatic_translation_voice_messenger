from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from models import db
    from routers.authentication import login_manager, bcrypt
    from routers.socketio import socketio
    
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    from routers import authentication
    from routers import home
    from routers.api import room
    
    app.register_blueprint(authentication.router)
    app.register_blueprint(home.router)
    app.register_blueprint(room.router)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)