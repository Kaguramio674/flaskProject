from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length, Regexp, ValidationError

from my_app.models import User


class SignupForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(min=6, max=15)])
    email = EmailField('Email address', [Email(message='Not a valid email address.'), DataRequired()])
    password = PasswordField('Password', [DataRequired(), Regexp(
        regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}',
        message='Please follow the password instruction.')])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords not match')])

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')

    def validate_username(self, username):
        users = User.query.filter_by(username=username.data).first()
        if users is not None:
            raise ValidationError('Username has been registered')


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account found with that email address.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError('No account found with that email address.')
        if not user.check_password(password.data):
            raise ValidationError('Incorrect password.')