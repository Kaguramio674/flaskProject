from flask import Blueprint, render_template, abort

from my_app.models import User

profile_bp = Blueprint('profile', __name__, url_prefix='/user')


@profile_bp.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('profile.html', title="Profile", user=user)
