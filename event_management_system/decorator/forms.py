from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

from event_management_system.decorator.validation import number_input_validation


class AddCategoryForm(FlaskForm):
    """Decorator add category form"""
    decoration_type = StringField('Category Title', validators=[DataRequired(), Length(min=2, max=20)])
    category_charges = IntegerField('Charges', validators=[DataRequired(),number_input_validation])
    submit = SubmitField('Submit')
