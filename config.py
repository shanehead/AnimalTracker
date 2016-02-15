import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SITE_NAME = 'Animal Tracker'
	WTF_CSRF_ENABLED = True
	SECRET_KEY = 'q\\r8^!@uLcw/z90|y{c,6B56q2vw!mlG'
	SQLALCHEMY_TRACK_MODIFICATIONS=True
	if os.environ.get('DATABASE_URL') is None:
		SQLALCHEMY_DATABASE_URI = "postgresql:///animal_tracker"
	else:
		SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	GOOGLE_LOGIN_CLIENT_ID = '128739772730-itrb3b45v3nnu99sdk5e4h8tvrkp2t4b.apps.googleusercontent.com'
	GOOGLE_LOGIN_CLIENT_SECRET = 'iGPd2eQQFQRuXXItlUUc19UI'
	OATH_CREDENTIALS = {'google':
						   {'id': GOOGLE_LOGIN_CLIENT_ID,
							'secret': GOOGLE_LOGIN_CLIENT_SECRET}}

	AWS_ACCESS_KEY_ID = 'AKIAIGMQZEO2BX4W7Q3Q'
	AWS_SECRET_ACCESS_KEY = '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'
	S3_BUCKET_NAME = 'animal-tracker'
	S3_UPLOAD_DIRECTORY = 'uploads'
	BOWER_COMPONENTS_ROOT = 'bower_components'

	#Email
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_SSL = False
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'shane.head@gmail.com'
	MAIL_PASSWORD = 'jcykdcwbowmbxabi'

class DevConfig(Config):
	ASSETS_DEBUG = True
	DEBUG = True
	WTF_CSRF_ENABLED = False
	if os.environ.get('DATABASE_URL') is None:
		SQLALCHEMY_DATABASE_URI = "postgresql:///animal_tracker_dev"
	else:
		SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class TestConfig(Config):
	TESTING = True
	WTF_CSRF_ENABLED = False
	if os.environ.get('DATABASE_URL') is None:
		SQLALCHEMY_DATABASE_URI = "postgresql:///animal_tracker"
	else:
		SQLALCHEMY_DATABASE_URI = "postgresql:///animal_tracker_test"
