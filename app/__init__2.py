#Initializing the Flask application.
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['Secret Key'] = 'this is a secret key'
    
    from .routes import routes
    from .auth import auth
    
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app
