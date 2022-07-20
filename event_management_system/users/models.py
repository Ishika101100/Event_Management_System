from flask import current_app
from flask_login import UserMixin
from itsdangerous import Serializer

from event_management_system import db, login_manager
from event_management_system.book_event.models import EventCategory


class User(db.Model, UserMixin):
    """add user in the database"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    venues = db.relationship("Venues", backref='venue_name', lazy=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    mobile_number = db.Column(db.String(12), nullable=False)
    address = db.Column(db.TEXT, nullable=False)
    user_type = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    caterer = db.relationship("Caterer", backref='user_get_caterer', cascade="all, delete-orphan", lazy="joined")
    decorator = db.relationship("Decorator", backref='user_get_decorator', cascade="all, delete-orphan", lazy="joined")
    event = db.relationship("Event", backref='Event_get_user', cascade="all, delete-orphan", lazy="joined")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


def commit_function():
    db.session.commit()


def add_function(value):
    db.session.add(value)


def delete_function(value):
    db.session.delete(value)


def get_user_type():
    return UserType.query.all()


def get_venue_type():
    return EventCategory.query.all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserType(db.Model):
    """add user type in the database"""
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), unique=True, nullable=False)
    user = db.relationship("User", backref='user_get_user_type', cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
        return self.user_type


def save_user(form, hashed_password=None):
    user = User(username=form.username.data, user_type=form.user_type.data, email=form.email.data,
                password=hashed_password,
                mobile_number=form.mobile_number.data, address=form.address.data)
    add_function(user)
    commit_function()
    return user


def get_user_from_email(email):
    return User.query.filter_by(email=email).first()
