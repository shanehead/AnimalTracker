from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from redis import Redis
from app.emails import send_alerts
import logging

logging.basicConfig()
redis_conn = Redis()
q = Queue(connection=redis_conn)

scheduler = BlockingScheduler()
@scheduler.scheduled_job('interval', hours=1)
def check_alerts():
	q.enqueue(send_alerts)

scheduler.start()
