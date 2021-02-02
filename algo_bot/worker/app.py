from celery import Celery

from algo_bot.settings import AlgoBotSettings, get_settings

settings: AlgoBotSettings = get_settings()
REDIS_URL = f"redis://{settings.redis_host}:{settings.redis_port}/0"

app: Celery = Celery("AlgoBot", broker=REDIS_URL, backend=REDIS_URL)
app.autodiscover_tasks(["algo_bot.worker.slack"])
