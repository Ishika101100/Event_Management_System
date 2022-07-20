from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from event_management_system.users.validation import phone_number_validation, password_validation, validate_username, \
    validate_email, validate_number, validate_email_exists, validate_update_username, validate_update_number


class RegistrationForm(FlaskForm):
    """Form for registering users"""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20), validate_username])
    user_type = StringField('user_type', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), validate_email])
    mobile_number = StringField('Mobile Number',
                                validators=[DataRequired(), Length(min=10, max=10), phone_number_validation,
                                            validate_number])
    address = TextAreaField("Address")
    password = PasswordField('Password', validators=[DataRequired(), password_validation])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


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
                           validators=[DataRequired(), Length(min=2, max=20), validate_update_username])
    mobile_number = StringField('Mobile Number',
                                validators=[DataRequired(), Length(min=10, max=10), phone_number_validation,
                                            validate_update_number])
    address = TextAreaField("Address")
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    change_Password = SubmitField('Change Password')
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    """Form for request reset users' password"""
    email = StringField('Email',
                        validators=[DataRequired(), Email(), validate_email_exists])
    submit = SubmitField('Request Password Reset')


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
