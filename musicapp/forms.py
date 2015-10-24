#!/usr/bin/python
import os
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, SubmitField, PasswordField, ValidationError, validators, FileField, HiddenField
from musicapp.models import User,Song
from flask import session
#from hello import db
#WTF_CSRF_CHECK_DEFAULT = False
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
			session['id'] = user.id
			session['email'] = user.email
			return True
		else:
			self.login.errors.append("Invalid username/e-mail or password")
			return False

class UploadForm(Form):
	name = TextField("Song Name", [validators.Required("Please enter a Title")])
	artist = TextField("Artist", [validators.Required("Please enter the Artist Name")])
	album = TextField("Album", [validators.Required("Please enter the Album Name")])
	#f = FileField("File", [validators.Required("Please select a file to upload")])
	fileurl = HiddenField("fileurl", [validators.Required("Please upload a file.")])
	#submit = SubmitField("Upload")
	
	
	songdata = ""
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
	def validate(self):
		if not Form.validate(self):
			return False
		self.songdata = self.name.data.lower() + '`' + self.album.data.lower() + '`' + self.artist.data.lower()
		song = Song.query.filter_by(songdata = self.songdata).first()
		if song:
			self.name.errors.append("Song already exists in database. Please choose another file.")
			return False
		else:
			return True
class ForgotPassForm(Form):
	email = TextField("Email", [validators.Required("Please enter an email address"), validators.Email("Please enter a valid email address")])
	submit = SubmitField("Reset Password")
	def __inint__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
	def validate(self):
		if not Form.validate(self):
			return False
		user = User.query.filter_by(email=email).first()
		if not user:
			self.email.errors.append("Email address not registered. Please sign up for a new account.")
			return False
		else:
			return True