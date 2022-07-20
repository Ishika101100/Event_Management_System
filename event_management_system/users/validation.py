import re

from flask_login import current_user
from wtforms import ValidationError

from event_management_system.users.models import User


def validate_username(self, field):
    """Validates if provided username exists in the database or not."""
    user = User.query.filter_by(username=field.data).first()
    if user:
        raise ValidationError('That username is taken. Please choose a different one.')


def validate_update_username(self, field):
    """Validates if provided username exists in the database or not."""
    if field.data != current_user.username:
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


def validate_email(self, field):
    """Validates if provided email exists in the database or not."""
    user = User.query.filter_by(email=field.data).first()
    if user:
        raise ValidationError('That email is taken. Please choose a different one.')


def validate_email_exists(self, field):
    user = User.query.filter_by(email=field.data).first()
    if user is None:
        raise ValidationError('There is no account with that email. You must register first.')


def validate_number(self, field):
    """Validates if provided mobile number exists in the database or not."""
    user = User.query.filter_by(mobile_number=field.data).first()
    if user:
        raise ValidationError('That mobile_number is taken. Please choose a different one.')


def validate_update_number(self, field):
    if field.data != current_user.mobile_number:
        user = User.query.filter_by(mobile_number=field.data).first()
        if user:
            raise ValidationError('That mobile_number is taken. Please choose a different one.')


def phone_number_validation(self, field):
    """phone number validation"""
    if field.data.isnumeric():
        regex = r'[7-9][0-9]{9}'
        if not (re.fullmatch(regex, field.data)):
            raise ValidationError("Invalid phone number")


def age_validation(self, field):
    """age validation"""
    if not field.data > 13:
        raise ValidationError("Age must be greater than 13")


def password_validation(self, field):
    """password validation"""
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$'
    if not re.fullmatch(regex, field.data):
        raise ValidationError("Password should consist One Capital Letter,Special Character,One Number,Length 8-18")
