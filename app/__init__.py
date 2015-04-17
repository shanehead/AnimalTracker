from flask import Flask
from flask.ext.login import LoginManager
from flask_googlelogin import GoogleLogin
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_thumbnails import Thumbnail
from flask.ext.qrcode import QRcode
from config import DevConfig
from momentjs import momentjs

app = Flask(__name__)
app.config.from_object(DevConfig)
app.jinja_env.globals['momentjs'] = momentjs
bootstrap = Bootstrap(app)
thumb = Thumbnail(app)
QRcode(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
googlelogin = GoogleLogin(app, lm)

from app import views, models