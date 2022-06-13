from app.tasks import celery


@celery.task(name="demo-task")
def demo(temp):
    return temp
