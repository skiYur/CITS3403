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
                return redirect(url_for('dashboard'))
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

        if password != confirm_password:
            flash('Passwords do not match',category= 'danger')
            return redirect(url_for('auth.sign_up'))
        else:
            user = User(username=username, email=email, password_hash=generate_password_hash('password1'))
            # user.set_password(password)
        # try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful', category='success')
            return redirect(url_for('auth.login'))
        # except Exception as e:
        #     flash(f'Error: {str(e)}', category='danger')
        #     return redirect(url_for('sign_up'))

    return render_template('sign_up.html')

@routes.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', category='success')
    return redirect(url_for('auth.login'))
