#!/usr/bin/python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from flask import render_template, request, flash, session, url_for, redirect
#WTF_CSRF_CHECK_DEFAULT = False
#from db import Table, Column, Integer, ForeignKey
#from db import relationship, backref

from musicapp.forms import ContactForm,SignupForm
from musicapp.models import User,Song
from musicapp import app,db

app.secret_key = 'development key'

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
			#return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
			if 'id' in session.keys():
				return "Please log out before creating new account"
			elif User.query.filter_by(email=form.email.data).first() != None:
				return "An account already exists with the email address provided."
			elif User.query.filter_by(username=form.username.data).all() != None:
				return "Nickname already exists, please use something else"
			else:
				user = User(form.data.username, form.data.email, form.data.password)
				db.session.add(user)
				db.session.commit()
				session['id'] = user.id
				return redirect(url_for('profile'))
	elif request.method == 'GET':
		return render_template('signup.html', form=form)
		
@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))
	
	user = User.query.filter_by(email = session['email']).first()
	
	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')