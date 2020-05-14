from apscheduler.schedulers.background import BackgroundScheduler
from .extract_records import add_new_record


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(add_new_record, 'cron', hour=17, minute=5)
    scheduler.start()