from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Length

from event_management_system.book_event.validation import validate_date


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    date = DateField('Date', validators=[DataRequired(), validate_date])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    no_of_guests = IntegerField('No of Guests', validators=[DataRequired()])
    submit = SubmitField('Book Event')


class UpdateForm(FlaskForm):
    """Form for updating Event Booking"""
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    no_of_guests = IntegerField('No of Guests', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired(), validate_date])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Update Event')
