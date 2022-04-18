from flask import Blueprint, render_template

forum_bp = Blueprint('forum', __name__)


@forum_bp.route('/forum')
def forum():
    return render_template('index.html', title="Forum")
