# verify_user.py
from app import app
from app.models import db, User

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Password Hash: {user.password_hash}, Salt: {user.salt}")
