#!/usr/bin/python
import os
from flask.ext.wtf import Form, validators
from wtforms import TextField, BooleanField, TextAreaField, SubmitField, PasswordField, ValidationError
from musicapp.models import User,Song
#from hello import db

class ContactForm(Form):
	name = TextField("Name")
	email = TextField("Email")
	subject = TextField("Subject")
	message = TextAreaField("Message")
	submit = SubmitField("Send")
class SignupForm(Form):
	firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
	lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
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
		else:
			return True