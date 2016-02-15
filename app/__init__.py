from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.qrcode import QRcode
from flask.ext.mail import Mail
from flask.ext.bower import Bower
from config import DevConfig
from momentjs import momentjs

def format_datetime(value, format='full'):
	if format == 'full':
		date_format = "%m/%d/%y %H:%M:%S"
	return value.strftime(date_format)

app = Flask(__name__)
app.config.from_object(DevConfig)
app.jinja_env.globals['momentjs'] = momentjs
app.jinja_env.filters['datetime'] = format_datetime
bootstrap = Bootstrap(app)
QRcode(app)
mail = Mail(app)
Bower(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models