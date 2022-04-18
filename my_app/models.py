from datetime import datetime

from flask_login import UserMixin

from my_app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    # first_name = db.Column(db.Text, nullable=False)
    # last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    member_since = db.Column(db.DateTime, default=datetime.utcnow())
    #friends = db.relationship("Friends", backref=db.backref('user'))

    def __repr__(self):
        return f"{self.id} {self.username} {self.email} {self.password} {self.member_since}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Friends(db.Model):
    __tablename__ = "friends"
    user_id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.user_id} {self.follower_id}"
