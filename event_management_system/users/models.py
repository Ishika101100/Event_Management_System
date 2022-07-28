from flask import current_app
from flask_login import UserMixin, current_user
from itsdangerous import Serializer

from event_management_system import db, login_manager


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

    @staticmethod
    def add_function(value):
        """function to add data in database"""
        db.session.add(value)

    @staticmethod
    def delete_function(value):
        """function to delete data in database"""
        db.session.delete(value)

    @staticmethod
    def commit_function():
        """function to commit data in database"""
        db.session.commit()

    def get_reset_token(self, expires_sec=1800):
        """
        user gets password reset token for changing password
        :param expires_sec: token expires in 1800 seconds
        :return: serializer with user_id
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        verify reset token
        :param token: passed by user
        :return: getting user's table where we get user_id
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    @login_manager.user_loader
    def load_user(user_id):
        """
        user_id for getting current user
        :return: User query where user_id is collected while login
        """
        return User.query.get(int(user_id))

    @classmethod
    def save_user(cls, form, hashed_password=None):
        """
        query to save user in database
        :param form: from the registration from
        :param hashed_password: None
        :return: user details of saved user
        """
        user = cls(username=form.username.data, user_type=form.user_type.data, email=form.email.data,
                   password=hashed_password,
                   mobile_number=form.mobile_number.data, address=form.address.data)
        cls.add_function(user)
        return user

    @classmethod
    def get_user_from_email(cls, email):
        """
        getting user details from provided email
        :param email: email of user
        :return: query by filtering user's email
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def validate_name(cls, username):
        """
        check if provided username exists or not in the user list
        :param username: from the provided username by user
        :return:query by filtering username
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def validate_email(cls, email):
        """
        check if provided email exists or not in the user list
        :param email: from the provided email by user
        :return:query by filtering email
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def validate_number(cls, mobile_number):
        """
        check if provided mobile_number exists or not in the user list
        :param mobile_number: from the provided mobile_number by user
        :return:query by filtering mobile_number
        """
        return cls.query.filter_by(mobile_number=mobile_number).first()

    @classmethod
    def update_account_function(cls, username, mobile_number, address):
        """
        user can update his/her account information
        :param username: from the update account form
        :param mobile_number:from the update account form
        :param address:from the update account form
        :return:save user details in the database
        """
        current_user.username = username
        current_user.mobile_number = mobile_number
        current_user.address = address
        cls.commit_function()

    @classmethod
    def update_image(cls, picture_file):
        """
        user can update his/her profile picture
        :param picture_file: from update account form
        :return: saves user's updated image
        """
        current_user.image_file = picture_file
        cls.commit_function()

    @classmethod
    def update_user_password(cls, hashed_password):
        """
        user can update/change his/her password
        :param hashed_password: password provided by the user
        :return: save user's hashed password in the database
        """
        current_user.password = hashed_password
        cls.commit_function()


class UserType(db.Model):
    """add user type in the database"""
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), unique=True, nullable=False)
    user = db.relationship("User", backref='user_get_user_type', cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
        return self.user_type

    @staticmethod
    def get_user_type():
        """
        getting different types for registering user
        :return: query for providing usertypes
        """
        return UserType.query.all()
