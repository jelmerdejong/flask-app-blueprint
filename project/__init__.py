# IMPORTS
from flask import Flask, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt 
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

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "users.login"

 
# BLUEPRINTS 
from project.textapi.views import textapi_blueprint
 
app.register_blueprint(textapi_blueprint,url_prefix="/textapi")

# ROUTES
@app.route('/', methods=['GET', 'POST']) 
def home():

    return render_template('textapi.html')


 
# from transformers import PreTrainedTokenizerFast
# tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
# bos_token='</s>', eos_token='</s>', unk_token='<unk>',
# pad_token='<pad>', mask_token='<mask>') 

# import torch
# from transformers import GPT2LMHeadModel
# model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
 