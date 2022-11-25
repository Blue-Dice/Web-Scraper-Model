from worker import celery_worker

@celery_worker.task(name='task_name')
def task():
    return "response"