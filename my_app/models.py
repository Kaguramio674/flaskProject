from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import ForeignKey

from my_app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    member_since = db.Column(db.DateTime, default=datetime.utcnow())
    profile = db.relationship("Profile", uselist=False, back_populates="user")

    def __repr__(self):
        return f"{self.id} {self.username} {self.email} {self.password} {self.member_since}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile(db.Model):
    __tablename__ = "profile"

    user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    username = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=True)
    last_name = db.Column(db.Text, nullable=True)
    gender = db.Column(db.Text, nullable=True)
    photo = db.Column(db.Text, nullable=True)
    user = db.relationship("User", back_populates="profile")


    def __repr__(self):
        return f"{self.id} {self.user_id} {self.username} {self.first_name} {self.last_name} {self.gender} {self.photo}"


