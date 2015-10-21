#!/usr/bin/python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash


class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(66))
	songs = relationship(Song, backref='user')

	def __init__(self,username,email,password):
		self.username = username
		self.email = email.lower()
		self.set_password(password)

	def __repr__(self):
		return '<User %r>' % self.username

	def set_password(self,password):
		self.pwdhash = generate_password_hash(password)
	def check_password(self,password):
		return check_password_hash(self.pwdhash, password)

	def get_song_list(self):
		pass

class Song(db.Model):
	songdata = Column(db.String(500), primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	link = Column(db.String(500))
	upvotes = Column(db.Integer)
	downvotes = Column(db.Integer)

	def __init__(self,songdata,link,user_id):
		self.upvotes = 0
		self.downvotes = 0
		self.songdata = songdata
		self.link = link
		self.user_id = user_id

	def __repr__(self):
		return '<Song %r>' % self.songdata
		
	def get_song_details(self):
		retval = {}
		retval['name'] = self.songdata[0]
		retval['album'] = self.songdata[1]
		retval['artist'] = self.songdata[2]
		return retval
		
	def upvote(user_id):
		self.upvotes += 1
	def downvote(user_id):
		self.downvote += 1