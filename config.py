import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SITE_NAME = 'Animal Tracker'
	WTF_CSRF_ENABLED = True
	SECRET_KEY = 'q\\r8^!@uLcw/z90|y{c,6B56q2vw!mlG'
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/animal_tracker"
	OPENID_PROVIDERS = [
		{'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
		{'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
	]
	MEDIA_URL = '/uploads'
	MEDIA_FOLDER = os.path.join(basedir, 'app' + MEDIA_URL)

class DevConfig(Config):
	ASSETS_DEBUG = True
	DEBUG = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/animal_tracker_dev"


class TestConfig(Config):
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/animal_tracker_test"
