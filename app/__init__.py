from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_qrcode import QRcode
from flask_mail import Mail
from flask_bower import Bower
from flask_restless import APIManager
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
api_manager = APIManager(app, flask_sqlalchemy_db=db)

from app import views, models