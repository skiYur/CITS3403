# app/models.py

import hashlib
import hmac
import os
from . import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(120), nullable=False, default='images/avatars/default_avatar.png')
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        """Create password hash with a random salt"""
        self.salt = os.urandom(32).hex()
        self.password_hash = self._generate_hash(password, self.salt)

    def check_password(self, password):
        """Verify password hash"""
        return hmac.compare_digest(self.password_hash, self._generate_hash(password, self.salt))

    def _generate_hash(self, password, salt):
        """Generate hash using SHA-256 and the provided salt"""
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    drink_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    super_likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reaction = db.Column(db.String(20), nullable=False)
    user = db.relationship('User', backref=db.backref('reactions', lazy=True))
    post = db.relationship('Post', backref=db.backref('reactions', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='_user_post_uc'),
    )
