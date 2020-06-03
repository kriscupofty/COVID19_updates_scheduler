from apscheduler.schedulers.background import BackgroundScheduler
from .extract_records import add_new_record
import logging


def start():
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler = BackgroundScheduler(job_defaults={'misfire_grace_time': 15*60})
    scheduler.add_job(add_new_record, 'cron', hour='17', minute='05')
    scheduler.start()