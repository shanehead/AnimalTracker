from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask_bootstrap3 import Bootstrap
from config import basedir, DevConfig
from momentjs import momentjs
import os

app = Flask(__name__)
app.config.from_object(DevConfig)
app.jinja_env.globals['momentjs'] = momentjs
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models