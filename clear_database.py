# clear_database.py

from app import create_app, db
from app.models import User, Post

def clear_database():
    app = create_app()
    with app.app_context():
        try:
            # Delete all records from the Post table
            Post.query.delete()
            # Delete all records from the User table
            User.query.delete()
            # Commit the changes
            db.session.commit()
            print("All users and posts have been removed from the database.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    clear_database()
