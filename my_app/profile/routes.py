from flask import Blueprint, render_template, abort, request, session
from flask_login import current_user

from my_app import db
from my_app.models import User
from my_app.profile.forms import BasicForm, PasswordForm

profile_bp = Blueprint('profile', __name__, url_prefix='/user')


@profile_bp.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('profile.html', title="Profile", user=user)


@profile_bp.route('/edit_basic', methods=['GET', 'POST'])
def edit_basic_profile():
    basic_form = BasicForm(request.form)
    if basic_form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if len(basic_form.first_name.data) > 0 and len(basic_form.last_name.data) > 0:
            user.profile.first_name = basic_form.first_name.data
            user.profile.last_name = basic_form.last_name.data
        if basic_form.gender.data:
            user.profile.gender = basic_form.gender.data
        db.session.commit()
    return render_template('edit_profile.html', title="Edit_Profile", user=current_user, form=basic_form)

@profile_bp.route('/password', methods=['GET', 'POST'])
def edit_password():
    password_form = PasswordForm(request.form)
    if password_form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.set_password(password_form.password_new.data)
        db.session.commit()
    return render_template('edit_password.html', title="Edit_Profile", user=current_user, form=password_form)

