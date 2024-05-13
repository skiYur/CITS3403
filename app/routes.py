from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('homepage.html')
    #return redirect(url_for('auth.login'))

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['email']  # Can be either username or email
        password = request.form['password']

        user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()

        if user:
            if user.check_password(password):
                session['username'] = user.username
                flash('Login successful', category='success')
                return redirect(url_for('routes.home'))  # Change here from 'routes.dashboard' to 'routes.home'
            else:
                flash('Incorrect password', category='danger')
        else:
            flash('Invalid username or email', category='danger')

    return render_template('login.html')

@routes.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Hello, {session['username']}!"
    else:
        flash('Please log in to access this page', category='danger')
        return redirect(url_for('auth.login'))

@routes.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password1']
        confirm_password = request.form['password2']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', category='danger')
            return redirect(url_for('routes.sign_up'))

        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists', category='danger')
            return redirect(url_for('routes.sign_up'))

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)

        # Commit the new user to the database
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful', category='success')
            return redirect(url_for('routes.login'))
        except Exception as e:
            flash(f'Error: {str(e)}', category='danger')
            return redirect(url_for('routes.sign_up'))

    return render_template('sign_up.html')

@routes.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', category='success')
    return redirect(url_for('auth.login'))


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
