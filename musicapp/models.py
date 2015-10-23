#!/usr/bin/python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from musicapp import db
from flask import session
WTF_CSRF_CHECK_DEFAULT = False
#from db import Table, Column, Integer, ForeignKey
#from db import relationship, backref
#from sqlalchemy.orm import relationship, backref
#from sqlalchemy.ext.declarative import declarative_base


class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	songdata = db.Column(db.String(500), db.ForeignKey('song.songdata'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	vote = db.Column(db.Integer)
	def __init__(self,songdata,user_id,vote):
		self.songdata = songdata
		self.user_id = user_id
		self.vote = vote
	def __repr__(self):
		return '<Vote %r>' % self.songdata + str(": ") + str(self.vote) + str("by ") + str(self.user_id)

class Song(db.Model):
	songdata = db.Column(db.String(500), primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	link = db.Column(db.String(500))
	upvotes = db.Column(db.Integer)
	downvotes = db.Column(db.Integer)

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
		retval['name'] = self.songdata.split("`")[0]
		retval['album'] = self.songdata.split("`")[1]
		retval['artist'] = self.songdata.split("`")[2]
		return retval
	
		
	def upvote(self,user_id):
		vote = Vote.query.filter_by(user_id=user_id,songdata=self.songdata).first()
		if vote:
			if vote.vote==-1:
				self.upvotes += 1
				self.downvotes -= 1
				vote.vote = 1
				db.session.commit()
				
		else:
			vote = Vote(self.songdata,user_id,1)
			self.upvotes += 1
			db.session.add(vote)
			db.session.commit()
		return (self.upvotes,self.downvotes)
			
	def downvote(self,user_id):
		vote = Vote.query.filter_by(user_id=user_id,songdata=self.songdata).first()
		if vote:
			if vote.vote==1:
				vote.vote = -1
				self.upvotes -= 1
				self.downvotes += 1
				db.session.commit()
		else:
			vote = Vote(self.songdata,user_id,-1)
			self.downvotes += 1
			db.session.add(vote)
			db.session.commit()
		return (self.upvotes,self.downvotes)

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(66))
	songs = db.relationship(Song, backref='user')
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

def get_user(song):
	return User.query.filter_by(id=song.user_id).first().username