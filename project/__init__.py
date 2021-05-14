# IMPORTS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required
from flask_mail import Mail
import os
from dotenv import load_dotenv 
load_dotenv(verbose=True)
import redis
from rq import Queue

import redis
from rq import Queue
import time

r = redis.Redis()
q = Queue(connection=r)

# CONFIG
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from project.models import User, Items


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


# BLUEPRINTS
from project.users.views import users_blueprint 
from project.textapi.views import textapi_blueprint

app.register_blueprint(users_blueprint,url_prefix="/users") 
app.register_blueprint(textapi_blueprint,url_prefix="/textapi")

# ROUTES
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """Render homepage"""

    all_user_items = Items.query.filter_by(user_id=current_user.id)
    return render_template('home.html', items=all_user_items)


# ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(410)
def page_gone(e):
    return render_template('410.html'), 410


from transformers import PreTrainedTokenizerFast
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
bos_token='</s>', eos_token='</s>', unk_token='<unk>',
pad_token='<pad>', mask_token='<mask>') 

import torch
from transformers import GPT2LMHeadModel
model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
