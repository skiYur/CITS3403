#from app import create_app()
from flask import Blueprint

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return "<h1> TEST </h1>"
    #return render_template('Project.html')
