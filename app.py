"""Simple App Blueprint: Basic"""

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Notes
from forms import NotesForm


@app.route('/', methods=['GET', 'POST'])
def home():
    """Render homepage"""

    errors = []
    note = {}

    if request.method == 'POST':
        # Get form input
        title = request.form['title']
        text = request.form['text']

        # Add to the database
        try:
            note = Notes(title, text)
            db.session.add(note)
            db.session.commit()
        except:
            errors.append("Unable to add item to database.")

    form = NotesForm(request.form)
    notes = Notes.query.all()

    return render_template('home.html', errors=errors, form=form, notes=notes)


if __name__ == '__main__':
    app.run()
