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
    BOWER_COMPONENTS_ROOT = 'bower_components'
    GOOGLE_PROJECT_ID = 'animal-tracker-1229'
    # SERVER_NAME = os.environ.get('SERVER_NAME', 'http://animal-tracker-1229')
    CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET', 'animal-tracker-1229.appspot.com')
    CLOUD_STORAGE_URL = 'https:/storage.googleapis.com/' + CLOUD_STORAGE_BUCKET

    #Email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

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
