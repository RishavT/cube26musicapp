from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
#UPLOAD_FOLDER = './tmp'
#if not os.path.exists(UPLOAD_FOLDER):
	#os.makedirs(UPLOAD_FOLDER)
	

ALLOWED_EXTENSIONS = set(['mp3'])




app.debug = True
if "DATABASE_URL" not in os.environ.keys():
	os.environ['DATABASE_URL'] = "postgresql://rishav:loller@localhost:5432/rishav"
if os.environ['DATABASE_URL'] == "":
	os.environ['DATABASE_URL'] = "postgresql://rishav:loller@localhost:5432/rishav"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.secret_key = 'development key'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
#db = []

from musicapp.routes import *
from musicapp.models import *
