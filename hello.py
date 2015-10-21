#!/usr/bin/python

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

from models.py import *
from views.py import *

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


	




##MainPage
@app.route('/')
def hello():
	return 'Hello World!'