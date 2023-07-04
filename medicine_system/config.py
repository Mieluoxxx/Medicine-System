from flask import Flask
from flask_sqlalchemy import SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql123@localhost/flask'

