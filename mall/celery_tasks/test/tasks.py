from celery_tasks.celery import app


@app.task(bind=True)
def sum(self, a, b):
    return a + b
