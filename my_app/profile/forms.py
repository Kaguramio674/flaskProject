from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, ValidationError

from my_app.models import User

CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Robot', 'Robot'), ('None', 'not prefer to say')]


class BasicForm(FlaskForm):
    first_name = StringField('First name', [Length(max=15)])
    last_name = StringField('Last name', [Length(max=15)])
    gender = SelectField('Gender', choices=CHOICES)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', [DataRequired()])
    password_new = PasswordField('Password', [DataRequired(), Regexp(
        regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}',
        message='Please follow the password instruction.')])
    password_repeat_new = PasswordField(label='Repeat Password',
                                        validators=[DataRequired(), EqualTo('password_new', message='Passwords not match')])

    def validate_password(self, password):
        user = User.query.filter_by(username=current_user.username).first()
        if not user.check_password(password.data):
            raise ValidationError('Incorrect password.')
