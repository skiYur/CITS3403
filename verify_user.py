from app import create_app, db
from app.models import User

# Create the app instance
app = create_app()

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Password Hash: {user.password_hash}, Salt: {user.salt}")
