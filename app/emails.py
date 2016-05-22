from app import app, db, mail
from flask.ext.mail import Message
from app.models import User, Alert
from sqlalchemy import extract, cast, Integer
from sqlalchemy.sql import func
from datetime import datetime

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    with app.app_context():
        mail.send(msg)

def send_alerts():
    # Grab all alerts within the last hour (since our schedule is hourly
    now = datetime.now()
    alerts = db.session.query(Alert).join(User).\
                        filter(Alert.start_date < now).\
                        filter((Alert.end_date == None) | (Alert.end_date > now)).\
                        filter(extract('hour', Alert.start_date) >= (now.hour - 1)).\
                        filter(extract('hour', Alert.start_date) < now.hour).\
                        filter(((Alert.repeat_period == 'days')
                                    & ((cast(extract('days', func.age(now, Alert.start_date)), Integer)
                                        % Alert.repeat_number) == 0))
                                | ((Alert.repeat_period == 'weeks')
                                    & ((cast(extract('days', func.age(now, Alert.start_date)), Integer)
                                        % (Alert.repeat_number*7)) == 0))
                                | ((Alert.repeat_period == 'months')
                                    & ((cast(extract('months', func.age(now, Alert.start_date)), Integer)
                                        % Alert.repeat_number) == 0)
                                    & (cast(extract('days', func.age(now, Alert.start_date)), Integer) == 0))
                                | ((Alert.repeat_period == 'years')
                                    & ((cast(extract('years', func.age(now, Alert.start_date)), Integer)
                                        % Alert.repeat_number) == 0)
                                    & ((cast(extract('months', func.age(now, Alert.start_date)), Integer) %
                                             Alert.repeat_number) == 0)
                                    & (cast(extract('days', func.age(now, Alert.start_date)), Integer) == 0))).\
                        all()
    for alert in alerts:
        print "Sending alert '%s'" % alert.name
        send_email(alert.name, app.config['MAIL_USERNAME'], [alert.user.email], alert.message, '')
