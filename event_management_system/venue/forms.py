from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired

from event_management_system.venue.validation import number_input_validation


class VenueInfo(FlaskForm):
    """Form for venue updating venue info"""
    venue_capactity = IntegerField('Venue Capacity', validators=[DataRequired(), number_input_validation])
    venue_charge = IntegerField('Venue Charge', validators=[DataRequired(), number_input_validation])
    submit = SubmitField('Update')
