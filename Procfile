web: gunicorn runp-heroku:app
init: python migrate.py db upgrade
upgrade: python migrate.py db migrate