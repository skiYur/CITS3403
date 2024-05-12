from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this-is-a-unique-secret-key'  # Updated key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not os.path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
