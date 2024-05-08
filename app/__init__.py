from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Find the absolute path
base_dir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(base_dir, '..', 'Project.SQLite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

from app.models import db
db.init_app(app)

with app.app_context():
    db.create_all()

from app import routes
