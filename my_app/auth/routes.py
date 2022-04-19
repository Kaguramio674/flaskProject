from datetime import timedelta
from sqlite3 import IntegrityError
from urllib.parse import urlparse, urljoin
from datetime import datetime
from flask_login import login_user, login_required, logout_user

from my_app import login_manager
from flask import Blueprint, render_template, flash, redirect, url_for, request, abort

from my_app import db
from my_app.auth.forms import SignupForm, LoginForm
from my_app.models import User, Profile

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm(request.form)
    if signup_form.validate_on_submit():
        user = User(username=signup_form.username.data, email=signup_form.email.data, member_since=datetime.utcnow())
        user.set_password(signup_form.password.data)
        db.session.add(user)
        db.session.commit()
        profile = Profile(user_id=user.id, username=user.username, photo="/static/img/default-user.jpg")
        db.session.add(profile)
        db.session.commit()
        try:
            flash(f"Hello, {user.username},  {user.email} You are signed up.",'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {signup_form.email.data}. ', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('auth.login'))
    return render_template('signup.html', title='Sign Up', form=signup_form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        login_user(user, remember=login_form.remember.data, duration=timedelta(minutes=1))
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main.index'))
    return render_template('login.html', title='Login', form=login_form)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.', 'warning')
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
