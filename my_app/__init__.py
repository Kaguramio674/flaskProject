from flask import Flask, render_template
from flask.helpers import get_root_path
from flask_login import LoginManager, login_required
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
import dash
import dash_bootstrap_components as dbc
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
moment = Moment()
photos = UploadSet('photos', IMAGES)

def create_app(config_classname):
    app = Flask(__name__)

    app.config.from_object(config_classname)
    db.init_app(app)
    configure_uploads(app, photos)
    moment.init_app(app)
    register_dashapp(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from my_app.models import User, Profile
        db.create_all()

    from my_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from my_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from my_app.profile.routes import profile_bp
    app.register_blueprint(profile_bp)

    from my_app.list.routes import user_list_bp
    app.register_blueprint(user_list_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def not_found(e):
        return render_template('500.html'), 500

    return app


def register_dashapp(app):
    from my_app.dash_app import layout
    from my_app.dash_app.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = dash.Dash(__name__,
                        server=app,
                        url_base_pathname='/dashboard/',
                        assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                        meta_tags=[meta_viewport],
                        external_stylesheets=[dbc.themes.SKETCHY])

    with app.app_context():
        dashapp.title = 'Dashboard'
        dashapp.layout = layout.layout
        register_callbacks(dashapp)

    _protect_dash_views(dashapp)


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
