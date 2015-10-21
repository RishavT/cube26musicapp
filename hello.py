#!/usr/bin/python

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(66))
	
	def __init__(self,username,email,password):
		self.username = username
		self.email = email.lower()
		self.set_password(password)
	def set_password(self,password):
		self.pwdhash = generate_password_hash(password)
	def check_password(self,password):
		return check_password_hash(self.pwdhash, password)
	def __repr__(self):
		return '<User %r' % self.username




##MainPage
@app.route('/')
def hello():
	return 'Hello World!'