from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import os
def get_name(string):
	return string.strip().split('`')[0].title()
def get_album(string):
	return string.strip().split('`')[1].title()
def get_artist(string):
	return string.strip().split('`')[2].title()
def length(x):
	return len(x)

app = Flask(__name__)
#UPLOAD_FOLDER = './tmp'
#if not os.path.exists(UPLOAD_FOLDER):
	#os.makedirs(UPLOAD_FOLDER)
	

ALLOWED_EXTENSIONS = set(['mp3'])
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET')



app.debug = True
if "DATABASE_URL" not in os.environ.keys():
	os.environ['DATABASE_URL'] = "postgresql://rishav:loller@localhost:5432/rishav"
if os.environ['DATABASE_URL'] == "":
	os.environ['DATABASE_URL'] = "postgresql://rishav:loller@localhost:5432/rishav"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.secret_key = 'development key'
app.jinja_env.filters['get_artist'] = get_artist
app.jinja_env.filters['get_album'] = get_album
app.jinja_env.filters['get_name'] = get_name
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
#db = []

from musicapp.routes import *
from musicapp.models import *

app.jinja_env.filters['get_user'] = get_user
app.jinja_env.filters['get_user'] = get_user
