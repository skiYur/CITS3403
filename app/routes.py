from flask import Blueprint, render_template, redirect, request, url_for, flash, session, jsonify
from .models import User, Post
from . import db
from datetime import datetime
from functools import wraps
import os
from flask import current_app, url_for
from werkzeug.utils import secure_filename
from .forms import UploadAvatarForm



routes = Blueprint('routes', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in or sign up to access this page.', category='danger')
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

@routes.route('/')
def home():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user:
            user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
            form = UploadAvatarForm()
            return render_template('homepage.html', user=user, isLoggedIn=True, user_posts=user_posts, form=form)
        else:
            flash('User not found', category='danger')
            return redirect(url_for('routes.login'))
    else:
        return redirect(url_for('routes.login'))

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('email')  
        password = request.form.get('password')

        user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
        if user and user.check_password(password):
            session['username'] = user.username
            session['user_id'] = user.id
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

        user = User(username=username, email=email, created_at=datetime.utcnow(), avatar='images/avatars/default_avatar.png')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful', category='success')
        return redirect(url_for('routes.login'))

    return render_template('sign_up.html')

@routes.route('/api/leaderboard')
def api_leaderboard():
    users = User.query.outerjoin(Post).group_by(User.id).order_by(db.func.count(Post.id).desc()).all()
    return jsonify([
        {"username": user.username, "postsCount": user.posts.count()} for user in users
    ])

@routes.route('/vodka')
@login_required
def vodka():
    recent_reviews = Post.query.filter_by(drink_type='vodka').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Vodka', reviews=recent_reviews)

@routes.route('/whisky')
@login_required
def whisky():
    recent_reviews = Post.query.filter_by(drink_type='whisky').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Whisky/Whiskey', reviews=recent_reviews)

@routes.route('/gin')
@login_required
def gin():
    recent_reviews = Post.query.filter_by(drink_type='gin').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Gin', reviews=recent_reviews)

@routes.route('/rum')
@login_required
def rum():
    recent_reviews = Post.query.filter_by(drink_type='rum').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Rum', reviews=recent_reviews)

@routes.route('/tequila')
@login_required
def tequila():
    recent_reviews = Post.query.filter_by(drink_type='tequila').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Tequila', reviews=recent_reviews)

@routes.route('/liqueur')
@login_required
def liqueur():
    recent_reviews = Post.query.filter_by(drink_type='liqueur').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Liqueur', reviews=recent_reviews)

@routes.route('/other')
@login_required
def other():
    recent_reviews = Post.query.filter_by(drink_type='other').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Other', reviews=recent_reviews)

@routes.route('/nonalcoholic')
@login_required
def nonalcoholic():
    recent_reviews = Post.query.filter_by(drink_type='nonalcoholic').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Non-alcoholic', reviews=recent_reviews)

@routes.route('/leaderboard')
@login_required
def leaderboard():
    return render_template('leaderboard.html')

@routes.route('/submit_review/<drink_type>', methods=['POST'])
@login_required
def submit_review(drink_type):
    drink_name = request.form.get('drinkName')
    instructions = request.form.get('instructions')
    ingredients = request.form.get('ingredients')
    review_text = request.form.get('review')
    rating = request.form.get('rating')

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash('User not found', category='error')
        return redirect(url_for('routes.login'))

    content = f"Drink Name: {drink_name}, Rating: {rating}, Instructions: {instructions}, Ingredients: {ingredients}, Review: {review_text}"
    new_post = Post(content=content, user_id=user.id, drink_type=drink_type.lower(), created_at=datetime.utcnow())
    db.session.add(new_post)
    db.session.commit()

    flash('Review submitted successfully!', category='success')
    return redirect(url_for('routes.' + drink_type.lower()))  # Ensure this redirection is to a valid endpoint

@routes.route('/delete_review/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    review = Post.query.get(review_id)
    if review and review.user_id == session['user_id']:
        db.session.delete(review)
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 403  # Forbidden or not found

@routes.route('/api/login_status')
def login_status():
    is_logged_in = 'username' in session
    return jsonify(isLoggedIn=is_logged_in)

@routes.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    form = UploadAvatarForm()
    if form.validate_on_submit():
        file = form.avatar.data
        filename = secure_filename(file.filename)
        user = User.query.filter_by(username=session['username']).first()
        if user:
            avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(avatar_path)
            user.avatar = f'images/avatars/{filename}'
            db.session.commit()
            flash('Avatar uploaded successfully!', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('User not found', 'danger')
    return redirect(url_for('routes.home'))


@routes.route('/remove_avatar', methods=['POST'])
@login_required
def remove_avatar():
    user = User.query.filter_by(username=session['username']).first()
    if user:
        user.avatar = 'images/avatars/default_avatar.png'
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 404