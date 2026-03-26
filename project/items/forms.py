from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),
                                           Length(min=1, max=254)])
    notes = StringField('Notes')
