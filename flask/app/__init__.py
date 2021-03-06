from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
# lm = LoginManager()
# lm.init_app(app)
# lm.login_view = 'login'
# oid = OpenID(app, os.path.join(basedir,'tmp'))

# This line pulls in the important parts of the app:
from app import views, models
