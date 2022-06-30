from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class VenueInfo(FlaskForm):
    """Form for venue updating venue info"""
    venue_capactity = IntegerField('Venue Capacity', validators=[DataRequired()])
    venue_charge = IntegerField('Venue Charge', validators=[DataRequired()])
    submit = SubmitField('Update')
