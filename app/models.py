# models.py
import hashlib
import hmac
import os
from .import db

# db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # salt = db.Column(db.String(64), nullable=False)

    # def set_password(self, password):
    #     """Create password hash with a random salt"""
    #     self.salt = os.urandom(32).hex()
    #     self.password_hash = self._generate_hash(password, self.salt)

    # def check_password(self, password):
    #     """Verify password hash"""
    #     return hmac.compare_digest(self.password_hash, self._generate_hash(password, self.salt))

    # def _generate_hash(self, password, salt):
    #     """Generate hash using SHA-256 and the provided salt"""
    #     return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()