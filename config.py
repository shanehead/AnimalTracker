import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SITE_NAME = 'Animal Tracker'
	WTF_CSRF_ENABLED = True
	SECRET_KEY = 'q\\r8^!@uLcw/z90|y{c,6B56q2vw!mlG'

class DevConfig(Config):
	ASSETS_DEBUG = True
	WTF_CSRF_ENABLED = False


class TestConfig(Config):
	TESTING = True
	WTF_CSRF_ENABLED = False
