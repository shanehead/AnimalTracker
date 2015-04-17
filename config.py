import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SITE_NAME = 'Animal Tracker'
	WTF_CSRF_ENABLED = True
	SECRET_KEY = 'q\\r8^!@uLcw/z90|y{c,6B56q2vw!mlG'
	if os.environ.get('DATABASE_URL') is None:
		SQLALCHEMY_DATABASE_URI = "postgresql://localhost/animal_tracker"
	else:
		SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	MEDIA_URL = '/uploads'
	MEDIA_FOLDER = os.path.join(basedir, 'app' + MEDIA_URL)
	GOOGLE_LOGIN_CLIENT_ID='128739772730-itrb3b45v3nnu99sdk5e4h8tvrkp2t4b.apps.googleusercontent.com'
	GOOGLE_LOGIN_CLIENT_SECRET='iGPd2eQQFQRuXXItlUUc19UI'
	GOOGLE_LOGIN_REDIRECT_URI='http://head-animal-tracker.herokuapp.com/oauth2callback'

class DevConfig(Config):
	ASSETS_DEBUG = True
	DEBUG = True
	WTF_CSRF_ENABLED = False
	if os.environ.get('DATABASE_URL') is None:
		SQLALCHEMY_DATABASE_URI = "postgresql://localhost/animal_tracker"
	else:
		SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class TestConfig(Config):
	TESTING = True
	WTF_CSRF_ENABLED = False
	if os.environ.get('DATABASE_URL') is None:
		SQLALCHEMY_DATABASE_URI = "postgresql://localhost/animal_tracker"
	else:
		SQLALCHEMY_DATABASE_URI = "postgresql://localhost/animal_tracker_test"
