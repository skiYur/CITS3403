from flask import render_template, request, redirect, url_for, flash
from . import app
from .auth import sign_up_user, login_user

@app.route('/')
<<<<<<< Updated upstream
def index():
    return render_template('Project.html')
=======
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = login_user(username, password)
        flash(result)
        if 'successful' in result:
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template('signup.html')

        result = sign_up_user(username, email, password)
        flash(result)
        if 'successfully' in result:
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/forgot-password')
def forgot_password():
    return "Forgot password page (To be implemented)"
>>>>>>> Stashed changes
