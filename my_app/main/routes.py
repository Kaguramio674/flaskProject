from flask import Blueprint, render_template, flash
from flask_login import current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():

    return render_template('index.html', title="Home")
