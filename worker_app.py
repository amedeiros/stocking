from celery import Celery

app = Celery(broker='redis://redis:6379/0')


@app.task(queue="apples")
def add(x, y):
    return x + y


add.apply_async(args=[1, 2])
add.apply_async(args=[1, 2])
add.apply_async(args=[1, 2])
