from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
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
    socketio.init_app(app, cors_allowed_origins="*")
    
    with app.app_context():
        db.create_all()
    
    from routers import authentication
    from routers import home
    from routers.api import room
    
    app.register_blueprint(authentication.router)
    app.register_blueprint(home.router)
    app.register_blueprint(room.router)
    
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=8080,
        ssl_context=('wccert.pem', 'wccert.key'),
        # debug=True
    )