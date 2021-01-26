from celery.decorators import periodic_task
from celery import celery
from algo_bot.worker.app import app
from celery.schedules import crontab
from algo_bot.db.models import Screener

@app.task
def screener_task(screener_id):
    pass

@periodic_task(run_every=crontab("*/1 * * * *"))
def screener_fan_task():
    for screener in Screener.all():
        celery.add_periodic_task(crontab(screener.cron), screener_task.s(screener.id))
