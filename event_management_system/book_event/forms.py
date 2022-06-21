from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired
from event_management_system.book_event.utils import no_of_guests_validation, validate_date


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired(),validate_date])
    location = StringField('location', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    duration = TimeField('Duration', validators=[DataRequired()])
    no_of_guests = IntegerField('No of Guests',validators=[DataRequired(),no_of_guests_validation])
    submit = SubmitField('Book Event')
