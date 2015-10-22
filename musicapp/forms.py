#!/usr/bin/python
import os
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, SubmitField, PasswordField, ValidationError, validators
from musicapp.models import User,Song
from flask import session
#from hello import db
#WTF_CSRF_CHECK_DEFAULT = False
class ContactForm(Form):
	name = TextField("Name")
	email = TextField("Email")
	subject = TextField("Subject")
	message = TextAreaField("Message")
	submit = SubmitField("Send")
class SignupForm(Form):
	username = TextField("Username",  [validators.Required("Please a suitable Username. You will be identified by your Username.")])
	email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	submit = SubmitField("Create account")
 
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
 
	def validate(self):
		if not Form.validate(self):
			return False
		 
		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append("That email is already taken")
			return False
		elif User.query.filter_by(username = self.username.data).first():
			self.username.errors.append("That username is already taken")
		else:
			return True
class SigninForm(Form):
	login = TextField("Email or Username",  [validators.Required("Please enter your username or email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	submit = SubmitField("Sign In")
	
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		
	def validate(self):
		if not Form.validate(self):
			return False
			
		user = User.query.filter_by(email = self.login.data.lower()).first()
		if not user:
			user = User.query.filter_by(username = self.login.data).first()
		if user and user.check_password(self.password.data):
			session['username'] = user.username
			return True
		else:
			self.login.errors.append("Invalid username/e-mail or password")
			return False