# project/texts/views.py

# IMPORTS
from flask import render_template, Blueprint, request, redirect, url_for, flash, Markup
from flask_login import current_user, login_required
from project import db
from project.models import Texts

from project import q

# CONFIG
textapi_blueprint = Blueprint('textapi', __name__, template_folder='templates')



def input_data(param):
    print(param)
    
    pass

@textapi_blueprint.route('/view', methods=['GET', 'POST'])
def textview():
    return render_template('textapi.html')

# ROUTES
@textapi_blueprint.route('/list', methods=['GET', 'POST'])
def all_items():
    """Render homepage"""
    all_user_items = db.session.query(Texts)
    return {
        "items" : all_user_items
    }



@textapi_blueprint.route('/add', methods=['GET', 'POST'])
def add_item():
    try:
        # add queue from radio receiver 
        data = request.args.get("data")
        secret = request.args.get("secret")
        
        if secret == "sec123":
            param = {
                "data": data
            }
            q.enqueue(input_data,param)
            return "true"
        else:
            return {
                "success" : "false",
                "message": "secret not match"
            }
        
    except Exception as e:
         
        return {
            "message" :str(e)
        }
