from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from event_management_system.models import User
from event_management_system.users.utils import phone_number_validation, password_validation


class RegistrationForm(FlaskForm):
    """Form for registering users"""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    user_type = StringField('user_type', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    mobile_number = StringField('Mobile Number',
                                validators=[DataRequired(), Length(min=10, max=10), phone_number_validation])
    address = TextAreaField("Address")
    password = PasswordField('Password', validators=[DataRequired(), password_validation])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Validates if provided username exists in the database or not."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Validates if provided email exists in the database or not."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_number(self, mobile_number):
        """Validates if provided mobile number exists in the database or not."""
        user = User.query.filter_by(mobile_number=mobile_number.data).first()
        if user:
            raise ValidationError('That mobile_number is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """Form for logging users in"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """Form for updating users' account"""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    mobile_number = StringField('Mobile Number',
                                validators=[DataRequired(), phone_number_validation])
    address = TextAreaField("Address")
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    change_Password = SubmitField('Change Password')
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Validates if provided username exists in the database or not."""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_number(self, mobile_number):
        """Validates if provided mobile number exists in the database or not."""
        if mobile_number.data != current_user.mobile_number:
            user = User.query.filter_by(mobile_number=mobile_number.data).first()
            if user:
                raise ValidationError('That mobile_number is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    """Form for request reset users' password"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """Form for reset users' password"""
    password = PasswordField('Password', validators=[DataRequired(), password_validation])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ChangePasswordForm(FlaskForm):
    """Form for change users' password"""
    old_password = PasswordField('Old Password')
    password = PasswordField('Password', validators=[DataRequired(), password_validation])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')
