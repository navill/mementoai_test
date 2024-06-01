import os
from datetime import datetime

import yaml
from celery.schedules import crontab

from celery import Celery
from database import Database
from models.short import ShortModel

with open("config.yml") as f:
    result = yaml.full_load(f)
    broker = result["celery"]["broker"]
    db_config = result["db"]

db = Database(**db_config)
app = Celery('tasks', broker=os.environ.get("CELERY_BROKER", broker))


@app.task
def hard_delete_expired_keys():
    with db.session() as sess:
        sess.query(ShortModel).filter(ShortModel.delete_at != None).delete()
        sess.commit()


@app.task
def soft_delete_expired_keys():
    with db.session() as sess:
        sess.query(ShortModel).filter(ShortModel.expire_at < datetime.now()).update({'delete_at': datetime.now()})()
        sess.commit()


app.conf.beat_schedule = {
    "soft_delete-expired-key-every-10-minutes": {
        "task": "tasks.soft_delete_expired_keys",
        "schedule": crontab(minute="*/10")
    },
    "hard_delete-expired-key-every-sunday": {
        "task": "tasks.hard_delete_expired_keys",
        "schedule": crontab(day_of_week="sunday")
    }
}
