from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import os

app = Flask(__name__)





app.debug = True
if "DATABASE_URL" not in os.environ.keys():
	os.environ['DATABASE_URL'] = "postgresql://rishav:loller@localhost:5432/rishav"
if os.environ['DATABASE_URL'] == "":
	os.environ['DATABASE_URL'] = "postgresql://rishav:loller@localhost:5432/rishav"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
#db = []

from musicapp.routes import *
from musicapp.models import *
