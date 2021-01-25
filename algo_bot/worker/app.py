from celery import Celery

from algo_bot.settings import AlgoBotSettings, get_settings

settings: AlgoBotSettings = get_settings()

app = Celery(broker=f"redis://{settings.redis_host}:{settings.redis_port}/0")

app.autodiscover_tasks(["algo_bot.worker.tasks"])
