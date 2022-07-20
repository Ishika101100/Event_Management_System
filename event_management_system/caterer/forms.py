from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

from event_management_system.caterer.validation import number_input_validation


class CatererAddCategoryForm(FlaskForm):
    """Decorator add category form"""
    food_type = StringField('Category Title', validators=[DataRequired(), Length(min=2, max=20)])
    food_charges = IntegerField('Charges', validators=[DataRequired(), number_input_validation])
    submit = SubmitField('Submit')
