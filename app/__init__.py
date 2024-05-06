from flask import Flask

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

<<<<<<< Updated upstream
from app import route
=======
# Import and initialize the database
from .auth import create_user_table
create_user_table()

# Import routes
from . import routes
>>>>>>> Stashed changes
