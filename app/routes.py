#from app import create_app()
from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/trending')
def trending():
    return render_template('trending.html')

@routes.route('/mocktails')
def mocktails():
    return render_template('mocktails.html')
