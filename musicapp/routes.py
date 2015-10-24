	#!/usr/bin/python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash, secure_filename
from flask import render_template, request, flash, session, url_for, redirect
from boto.s3.connection import S3Connection, Bucket, Key

from hashlib import sha1
import time, os, json, base64, hmac, urllib, string, random

from musicapp.forms import SignupForm, SigninForm, UploadForm, ForgotPassForm
from musicapp.models import User, Song, Vote
from musicapp import app, db, ALLOWED_EXTENSIONS, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME
#import musicapp.fileupload as fileupload
import send_email
def playlist(html):
	song_count = Song.query.count()
	if song_count == 0:
		return render_template(html,empty=1)
	
	song_limit = 10
	if 'song_limit' in request.args:
		try:
			if int(request.args.get('song_limit')) in range(1,51):
				song_limit = int(request.args.get('song_limit'))
		except (TypeError, ValueError) as e:
			pass
	
	page = 0
	if 'page' in request.args:
		page = int(request.args.get('page'))
	order_by = 'upvotes'
	reverse = 0
	if 'reverse' in request.args:
		if request.args.get('reverse') in ['0','1']:
			reverse = int(request.args.get('reverse'))
	if 'sort' in request.args:
		if request.args['sort'] == 'songdata':
			order_by = 'songdata'
		elif request.args['sort'] == 'votes':
			order_by = 'upvotes' if reverse == 0 else 'downvotes'
		elif request.args['sort'] in ['upvotes','downvotes']:
			order_by = request.args['sort']
	temp_query = Song.query
	try:
		if 'search' in request.args:
			temp_query = temp_query.filter(Song.songdata.like('%' + request.args['search'].lower() + '%'))
		if 'user_id' in request.args:
			temp_query = temp_query.filter_by(user_id=int(request.args.get('user_id')))
		if order_by == 'upvotes':
			song_list = temp_query.order_by(Song.upvotes.desc()).offset(page).limit(song_limit).all()
		elif order_by == 'downvotes':
			song_list = temp_query.order_by(db.desc(Song.downvotes)).offset(page).limit(song_limit).all()
		else:
			song_list = temp_query.order_by(order_by).offset(page).limit(song_limit).all()
	except:
		song_list = Song.query.order_by(Song.upvotes.desc()).offset(page).limit(song_limit).all()
	"""if 'user_id' in request.args:
		try:
			if 'search' in request.args:
				temp_query = Song.query.filter(Song.songdata.like('%' + request.args['search'].lower() + '%'))
				temp_query = temp_query.filter_by(user_id=int(request.args.get('user_id')))
			else:
				temp_query = Song.query.filter_by(user_id=int(request.args.get('user_id')))
			if order_by == 'upvotes':
				song_list = temp_query.order_by(Song.upvotes.desc()).offset(page).limit(song_limit).all()
			elif order_by == 'downvotes':
				song_list = temp_query.order_by(db.desc(Song.downvotes)).offset(page).limit(song_limit).all()
			else:
				song_list = temp_query.filter_by(user_id=int(request.args.get('user_id'))).order_by(order_by).offset(page).limit(song_limit).all()
		except (TypeError, ValueError) as e:
			song_list = Song.query.order_by(order_by).offset(page).limit(song_limit).all()
	else:
		song_list = Song.query.order_by(order_by).offset(page).limit(song_limit).all()"""
	return render_template(html, song_list=song_list, User=User,empty=0, page=page, song_count=song_count)

@app.route('/')
def home():
	return playlist('home.html')

@app.route('/allsongs', methods=['GET'])
def allsongs():
	return playlist('allsongs.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact', methods=['GET'])
def contact():
	return render_template('contact.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
	if 'username' in session:
		return redirect(url_for('profile'))
	form = SignupForm()
	
	if request.method == 'POST':
		if not form.validate():
			return render_template('signup.html', form=form)
		else:
			#return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
			if 'username' in session.keys():
				return "Please log out before creating new account"
			elif User.query.filter_by(email=form.email.data).first() != None:
				return "An account already exists with the email address provided."
			elif User.query.filter_by(username=form.username.data).first() != None:
				return "Nickname already exists, please use something else"
			else:
				user = User(form.username.data, form.email.data, form.password.data)
				db.session.add(user)
				db.session.commit()
				session['username'] = user.username
				session['id'] = user.id
				session['email'] = user.email
				return redirect(url_for('profile'))
	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if 'username' in session:
		return redirect(url_for('profile'))
	form = SigninForm()
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signin.html', form=form)
		else:
			return redirect(url_for('profile'))
	elif request.method == 'GET':
		return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
	if 'username' in session.keys():
		session.pop('username')
	if 'id' in session.keys():
		session.pop('id')
	if 'email' in session.keys():
		session.pop('email')
	return redirect(url_for('home'))
		
@app.route('/profile')
def profile():
	if 'username' not in session:
		return redirect(url_for('signin'))
	
	user = User.query.filter_by(username = session['username']).first()
	if user is None:
		return redirect(url_for('signin'))
	else:
		song_count = len(user.songs)
		return render_template('profile.html', song_count=song_count)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	
	form = UploadForm()
	if request.method == 'GET':
		if 'username' not in session:
			return redirect(url_for('signin'))
		return render_template('upload.html', form=form)
	elif request.method == 'POST':
		if not form.validate():
			return render_template('upload.html', form=form)
			
		songdata = form.songdata
		fileurl = form.fileurl.data
		
		#Add song to database if not already present
		song = Song.query.filter_by(songdata = songdata).first()
		if not song:
			song = Song(songdata,fileurl,session['id'])
			db.session.add(song)
			db.session.commit()
		return render_template("notice.html", message="Song uploaded.", redirect="/allsongs?user_id="+str(session['id']))
		
			

@app.route('/sign_s3/')
def sign_s3():
	object_name = urllib.quote_plus(request.args.get('name').lower() + '`' + request.args.get('album').lower() + '`' + request.args.get('artist').lower() + '.mp3')
	mime_type = request.args.get('file_type')
	
	expires = int(time.time()+60*60*24)
	amz_headers = "x-amz-acl:public-read"
	
	string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET_NAME, object_name)
	print string_to_sign
	signature = base64.encodestring(hmac.new(AWS_SECRET_ACCESS_KEY.encode(), string_to_sign.encode('utf8'), sha1).digest())
	signature = urllib.quote_plus(signature.strip())
	
	url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET_NAME, object_name)
	#url = 'http://httpbin.org/put'
	content = json.dumps({
		'signed_request': '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (url, AWS_ACCESS_KEY_ID, expires, signature),
		'url': url,
	})
	return content


@app.route('/delete')
def delete():
	#try:
	songdata = request.args.get('songdata')
	
	song = Song.query.filter_by(songdata=songdata).first()
	votes = Vote.query.filter_by(songdata=song.songdata).all()
	for x in votes:
		db.session.delete(x)
	db.session.commit()
	db.session.delete(song)
	db.session.commit()
	
	try:
		conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

		b = Bucket(conn, S3_BUCKET_NAME)

		k = Key(b)

		k.key = songdata.lower() + '.mp3'
	except:
		pass

	b.delete_key(k)
	return render_template('notice.html', message="Delete successful.", redirect="/")
	#return render_template('notice.html', message="Could not process your request, pleast try again later.")

@app.route('/vote', methods=['GET','POST'])
def vote():
	retval = None
	if 'id' not in session:
		return signup()
	if 'songid' not in request.args:
		return "-1 nosongid"
	if 'vote' not in request.args:
		return "-1 novote"
	vote = request.args.get('vote')
	if vote not in ['-1','1']:
		return "-1 invalid vote"
	try:	
		songid = int(request.args.get('songid'))
	except Exception:
		return "-1 invalid songid"
	song = Song.query.filter_by(id=songid).first()
	if not song:
		return "-1" + songdata
	if vote == '1':
		retval = song.upvote(session['id'])
	else:
		retval = song.downvote(session['id'])
	db.session.commit()
	return str(retval[0]) + " " + str(retval[1])
	

@app.route('/cleanup', methods=['GET','POST'])
def cleanup():
	return "Cleanup Disabled"
	"""
	if 'id' not in session:
		return signin()
	if session['id'] != 1:
		return render_template('notice.html', message="You are not authorized to perform this action", redirect="/")
	conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = Bucket(conn, S3_BUCKET_NAME)
	for key in bucket.list():
		if 'static' in key.key:
			if key.key.index('static') == 0:
				continue
		if 'logs' in key.key:
			if key.key.index('logs') == 0:
				continue
		if Song.query.filter_by(songdata=key.key).first()==None:
			bucket.delete_key(key)
	return render_template('notice.html', message='Cleanup successful.', redirect='/')"""
@app.route('/changepassword', methods=['POST'])
def change_pass():
	if 'id' not in session:
		return signin()
	oldpass = request.form['oldpass']
	newpass = request.form['newpass']
	user = User.query.filter_by(id=session['id']).first()
	if user.check_password(oldpass):
		user.set_password(newpass)
		db.session.commit()
		return render_template('notice.html', message="Password changed successfully.", redirect=url_for('profile'))
	else:
		return render_template('notice.html', message='Invalid password, please try again', redirect=url_for('profile'))

@app.route('/forgotpassword', methods=['GET','POST'])
def forgot_pass():
	form = ForgotPassForm()
	if 'id' in session:
		return render_template('notice.html', message='Please sign out before proceeding.', redirect='/')
	if request.method == 'GET':
		return render_template('forgotpassword.html', form=form)
	else:
		user = User.query.filter_by(email=request.form['email']).first()
		
		password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(7))
		user.set_password(password)
		db.session.commit()
		send_email.send_email(user.email, password)
		
		return render_template('notice.html', message='Password reset. Please check your email address.',redirect='/')