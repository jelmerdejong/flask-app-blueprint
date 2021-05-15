# project/texts/views.py

# IMPORTS
from flask import render_template, Blueprint, request, redirect, url_for, flash, Markup, jsonify
from project import db
from project.models import Texts

from project import q
import base64
import secrets
# CONFIG
textapi_blueprint = Blueprint('textapi', __name__, template_folder='templates')



@textapi_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    all_user_items = Texts.query.all()
    tag = request.args.get('text')
    search = "%{}%".format(tag)
    texts = Texts.query.filter(Texts.texts.like(search)).all()
    return jsonify(texts)
    
    
@textapi_blueprint.route('/view', methods=['GET', 'POST'])
def textview():
    return render_template('textapi.html')

# ROUTES
@textapi_blueprint.route('/list', methods=['GET', 'POST'])
def all_items():
    """Render homepage"""
    if request.args.get("filter") == "all":
        items = Texts.query.all()
    else:
        
        items = db.session.query(Texts).filter(Texts.predicted_text == None).all()
    return jsonify(items) 

@textapi_blueprint.route('/add', methods=['GET', 'POST'])
def add_item():
    try:
        # add queue from radio receiver 
        data = request.args.get("data") 
        secret = request.args.get("secret")
        token = secrets.token_hex(nbytes=32) 
        if secret == "sec123":
            # redis queue
            
            new_text = Texts(token, data)
            db.session.add(new_text)
            db.session.commit()
            json_data = {
                "success": True,
                "message":"record created"
            }
            return jsonify(json_data)
        else:
            json_data = {
                "success" : "false",
                "message": "secret not match"
            }
            return jsonify(json_data) 
            

    except Exception as e:
        json_data = {
            "success" : "false",
            "message": "Exception"
        }
        return jsonify(json_data)


@textapi_blueprint.route('/delete/<items_id>') 
def delete_item(items_id):
    try:
        secret = request.args.get("secret")
        if secret == "sec123":
            item = Texts.query.filter_by(id=items_id).first_or_404()
            
            db.session.delete(item)
            db.session.commit() 
            
            json_data = {
                "success": True,
                "message":"deleted"
            }
            return jsonify(json_data)
        else:
            json_data = {
                "success": False,
                "message":"secret not match"
            }
            return jsonify(json_data)
    except Exception as e:
        json_data = {
            "success" : "false",
            "message": "Exception"
        }
        return jsonify(json_data)

# just update predicted text
@textapi_blueprint.route('/update/<items_id>') 
def update_item(items_id):
    try:
        secret = request.args.get("secret")
        data = request.args.get("data")
        
        if secret == "sec123":
            item = Texts.query.filter_by(id=items_id).first_or_404()
            item.predicted_text = data
            db.session.commit() 
            json_data = {
                "success": True,
                "message":"updated"
            }
            return jsonify(json_data)
        else:
            json_data = {
                "success": False,
                "message":"secret not match"
            }
            return jsonify(json_data)
    except Exception as e:
        json_data = {
            "success" : "false",
            "message": "Exception"
        }
        return jsonify(json_data)