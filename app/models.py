# models.py
from datetime import datetime
import hashlib
import hmac
import os
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(120), nullable=False, default='images/avatars/default_avatar.png')

    def set_password(self, password):
        self.salt = os.urandom(32).hex()
        self.password_hash = self._generate_hash(password, self.salt)

    def check_password(self, password):
        return hmac.compare_digest(self.password_hash, self._generate_hash(password, self.salt))

    def _generate_hash(self, password, salt):
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    drink_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    super_likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

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
