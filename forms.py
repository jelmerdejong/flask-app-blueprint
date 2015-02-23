from flask_wtf import Form
from wtforms import TextField


class NotesForm(Form):
    title = TextField('Title')
    text = TextField('Text')
