#!/usr/bin/python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from flask import render_template, request, flash
WTF_CSRF_CHECK_DEFAULT = False
#from db import Table, Column, Integer, ForeignKey
#from db import relationship, backref

from musicapp.forms import ContactForm,SignupForm
from musicapp.models import User,Song
from musicapp import app,db

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	form = ContactForm()
	
	if request.method == 'POST':
		return 'Form posted.'
	elif request.method == 'GET':
		return render_template('contact.html', form=form)

@app.route('/signup',methods=['GET','POST'])
def signup():
	form = SignupForm()
	
	if request.method == 'POST':
		if not form.validate():
			return render_template('signup.html', form=form)
		else:
			return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
	elif request.method == 'GET':
		return render_template('signup.html', form=form)