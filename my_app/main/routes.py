from flask import Blueprint, render_template

from my_app.models import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():

    return render_template('index.html', title="Home")
