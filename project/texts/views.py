# project/texts/views.py

# IMPORTS
from flask import render_template, Blueprint, request, redirect, url_for, flash, Markup
from flask_login import current_user, login_required
from project import db
from project.models import Texts

from project import q

# CONFIG
texts_blueprint = Blueprint('texts', __name__, template_folder='templates')



def input_data(param):
    # add to model, and 
    pass

@texts_blueprint.route('/view', methods=['GET', 'POST'])
def textview():
    return render_template('text.html')

# ROUTES
@texts_blueprint.route('/list', methods=['GET', 'POST'])
def all_items():
    """Render homepage"""
    all_user_items = Texts.query.all()
    return {
        "items" : all_user_items
    }



@texts_blueprint.route('/add', methods=['GET', 'POST'])
def add_item():
    form = ItemsForm(request.form)
    try:
        # add queue from radio receiver 
        data = request.args("data")
        secret = request.args("secret")
        
        if secret == "sec123":
            param = {
                "data": data
            }
            q.enqueue(input_data,param)
            return {
                "success" : True,
                "message": "added to queue"
            }
        else:
            return False
        
    except:
        db.session.rollback()
        message = Markup(
            "<strong>Oh snap!</strong>! Unable to add item.")
        flash(message, 'danger')

