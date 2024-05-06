import hashlib
import sqlite3
from datetime import datetime
import os

# Absolute path to the SQLite database file
db_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../Project.SQLite')

# Function to hash passwords using SHA256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Function to sign up a user
def sign_up_user(username: str, email: str, password: str) -> str:
    hashed_password = hash_password(password)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, hashed_password))

        conn.commit()
        conn.close()

        return "User signed up successfully."

    except sqlite3.IntegrityError as e:
        return f"Error: {str(e)}"

# Function to login a user
def login_user(username: str, password: str) -> str:
    hashed_password = hash_password(password)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, hashed_password))

    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login successful."
    else:
        return "Login failed. Invalid username or password."

# Create the users table
def create_user_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

# Create the users table (execute this once)
create_user_table()
