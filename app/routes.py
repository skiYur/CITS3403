from flask import Blueprint, render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Post, Reaction, db
from datetime import datetime
from werkzeug.utils import secure_filename
from .forms import UploadAvatarForm
import re
import os

routes = Blueprint('routes', __name__)

@routes.route('/')
@login_required
def home():
    user = User.query.filter_by(username=session.get('username')).first()
    if user:
        user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
        form = UploadAvatarForm()
        return render_template('homepage.html', user=user, isLoggedIn=True, user_posts=user_posts, form=form)
    else:
        flash('User not found', category='danger')
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
            login_user(user)  # Use login_user to log in the user with Flask-Login
            flash('Login successful', category='success')
            return redirect(url_for('routes.home'))
        else:
            flash('Invalid login credentials', category='danger')

    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    session.pop('user_id', None)
    flash('You have been logged out', category='success')
    return redirect(url_for('routes.login'))

def is_strong_password(password):
    """Check if the password is strong."""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

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

        if not is_strong_password(password):
            flash('Password must be at least 8 characters long, contain an uppercase letter, and a special character.', category='danger')
            return redirect(url_for('routes.sign_up'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if existing_user.username == username:
                flash('Username already exists', category='danger')
            if existing_user.email == email:
                flash('Email already exists', category='danger')
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
    users = User.query.outerjoin(Post).group_by(User.id).order_by(db.func.count(Post.id).desc()).limit(10).all()
    leaderboard = [
        {
            "username": user.username,
            "postsCount": len(user.posts),
            "avatar": url_for('static', filename=user.avatar)  # Use url_for to generate the full URL
        }
        for user in users
    ]
    return jsonify(leaderboard)

@routes.route('/vodka')
@login_required
def vodka():
    recent_reviews = Post.query.filter_by(drink_type='vodka').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Vodka', reviews=recent_reviews)

@routes.route('/whiskey')
@login_required
def whiskey():
    recent_reviews = Post.query.filter_by(drink_type='whiskey').order_by(Post.created_at.desc()).all()
    for review in recent_reviews:
        review.user = User.query.get(review.user_id)
    return render_template('drink_review.html', drink_type='Whiskey', reviews=recent_reviews)

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

@routes.route('/non_alcoholic')
@login_required
def non_alcoholic():
    recent_reviews = Post.query.filter_by(drink_type='non_alcoholic').order_by(Post.created_at.desc()).all()
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

    user = current_user  # Use current_user from Flask-Login
    if not user:
        flash('User not found', category='error')
        return redirect(url_for('routes.login'))

    content = f"Drink Name: {drink_name}, Rating: {rating}, Instructions: {instructions}, Ingredients: {ingredients}, Review: {review_text}"
    new_post = Post(content=content, user_id=user.id, drink_type=drink_type.lower().replace("-", "_"), created_at=datetime.utcnow())
    db.session.add(new_post)
    db.session.commit()

    flash('Review submitted successfully!', category='success')
    # Dynamically construct the endpoint name based on drink_type
    return redirect(url_for(f'routes.{drink_type.lower().replace("-", "_")}'))

@routes.route('/delete_review/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    review = Post.query.get(review_id)
    if review and review.user_id == current_user.id:
        # Delete reactions associated with the post
        Reaction.query.filter_by(post_id=review.id).delete()
        db.session.delete(review)
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 403

@routes.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    action = request.json.get('action')
    existing_reaction = Reaction.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing_reaction:
        if existing_reaction.reaction == action:
            db.session.delete(existing_reaction)
            update_post_reactions(post, action, -1)
        else:
            update_post_reactions(post, existing_reaction.reaction, -1)
            existing_reaction.reaction = action
            db.session.add(existing_reaction)
            update_post_reactions(post, action, 1)
    else:
        new_reaction = Reaction(user_id=current_user.id, post_id=post_id, reaction=action)
        db.session.add(new_reaction)
        update_post_reactions(post, action, 1)

    db.session.commit()
    return jsonify({
        'success': True,
        'likes': post.likes,
        'super_likes': post.super_likes,
        'dislikes': post.dislikes
    })

def update_post_reactions(post, reaction_type, delta):
    if reaction_type == 'like':
        post.likes += delta
    elif reaction_type == 'super_like':
        post.super_likes += delta
    elif reaction_type == 'dislike':
        post.dislikes += delta
    db.session.commit()

@routes.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    if query:
        users = User.query.filter(User.username.like(f'%{query}%')).all()
        if users:
            return render_template('search_results.html', users=users, query=query)
        else:
            flash('No users found', category='warning')
            return redirect(url_for('routes.home'))
    else:
        flash('Enter a username to search', category='warning')
        return redirect(url_for('routes.home'))

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

@routes.route('/api/leaderboard-position', methods=['GET'])
@login_required
def get_leaderboard_position():
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({"position": None}), 404

    users = User.query.outerjoin(Post).group_by(User.id).order_by(db.func.count(Post.id).desc()).all()
    position = next((index + 1 for index, u in enumerate(users) if u.id == user.id), None)
    
    return jsonify({"position": position})

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

@routes.route('/user/<username>')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found', category='danger')
        return redirect(url_for('routes.leaderboard'))

    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    return render_template('user_profile.html', user=user, user_posts=user_posts)

@routes.route('/api/popular_reviews')
def api_popular_reviews():
    reviews = Post.query.order_by((Post.likes + Post.super_likes).desc()).all()
    popular_reviews = [
        {
            "username": User.query.get(review.user_id).username,
            "avatar": url_for('static', filename=User.query.get(review.user_id).avatar),
            "drink_type": review.drink_type,
            "content": review.content,
            "likes": review.likes,
            "super_likes": review.super_likes,
            "total_likes": review.likes + review.super_likes
        }
        for review in reviews
    ]
    return jsonify(popular_reviews)

@routes.route('/popular-reviews')
@login_required
def popular_reviews():
    return render_template('popular_reviews.html')
