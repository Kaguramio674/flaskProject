from flask import Blueprint, render_template

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile')
def forum():
    return render_template('index.html', title="Profile")
