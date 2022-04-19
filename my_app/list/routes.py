from flask import Blueprint, render_template

from my_app.models import User

user_list_bp = Blueprint('list', __name__)


@user_list_bp.route('/user_list')
def user_list():
    for i in range(1,9000):
        if User.query.filter_by(id=i).first() is None:
            break
    return render_template('user_list.html', title="Home",User=User,size=i)
