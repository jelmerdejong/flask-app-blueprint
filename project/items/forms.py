from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class ItemsForm(FlaskForm):
    name = TextField('Name', validators=[DataRequired(), Length(min=1, max=254)])
    notes = TextField('Notes')

class EditItemsForm(FlaskForm):
    name = TextField('Name', validators=[DataRequired(), Length(min=1, max=254)])
    notes = TextField('Notes')
