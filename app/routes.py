from flask import Blueprint, render_template, redirect, request, url_for, flash, session, jsonify
from .models import User, Post
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user:
            print(f"DEBUG: User found: {user.username}")  # Debug statement
            return render_template('homepage.html', username=user.username)
        else:
            # Handle case where user is not found in the database
            flash('User not found', category='danger')
            return redirect(url_for('routes.login'))
    else:
        # Redirect to login if not logged in
        return redirect(url_for('routes.login'))

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('email')  
        password = request.form.get('password')

        user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
        if user and user.check_password(password):
            session['username'] = user.username
            flash('Login successful', category='success')
            print(f"DEBUG: Login successful for user: {user.username}")  # Debug statement
            return redirect(url_for('routes.home'))
        else:
            flash('Invalid login credentials', category='danger')
            print("DEBUG: Invalid login credentials")  # Debug statement

    return render_template('login.html')

@routes.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', category='success')
    print("DEBUG: User logged out")  # Debug statement
    return redirect(url_for('routes.login'))

@routes.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password1')
        confirm_password = request.form.get('password2')

        if password != confirm_password:
            flash('Passwords do not match', category='danger')
            return redirect(url_for('routes.sign_up'))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists', category='danger')
            return redirect(url_for('routes.sign_up'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful', category='success')
        print(f"DEBUG: Registration successful for user: {user.username}")  # Debug statement
        return redirect(url_for('routes.login'))

    return render_template('sign_up.html')

@routes.route('/api/leaderboard')
def api_leaderboard():
    users = User.query.outerjoin(Post).group_by(User.id).order_by(db.func.count(Post.id).desc()).all()
    return jsonify([
        {"username": user.username, "postsCount": user.posts.count()} for user in users
    ])

# Add routes for specific drink categories
@routes.route('/vodka')
def vodka():
    return render_template('drink_review.html', drink_type='Vodka')

@routes.route('/whisky')
def whisky():
    return render_template('drink_review.html', drink_type='Whisky/Whiskey')

@routes.route('/gin')
def gin():
    return render_template('drink_review.html', drink_type='Gin')

@routes.route('/rum')
def rum():
    return render_template('drink_review.html', drink_type='Rum')

@routes.route('/tequila')
def tequila():
    return render_template('drink_review.html', drink_type='Tequila')

@routes.route('/liqueur')
def liqueur():
    return render_template('drink_review.html', drink_type='Liqueur')

@routes.route('/other')
def other():
    return render_template('drink_review.html', drink_type='Other')

@routes.route('/nonalcoholic')
def nonalcoholic():
    return render_template('drink_review.html', drink_type='Non-alcoholic')

@routes.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
