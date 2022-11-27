from celery_config.celery_worker import CeleryWorker
from decouple import config
import sys

worker = CeleryWorker(config('REDIS_URL'))

# Define task routes: list of ['task_name','task_queue']
task_routes = (
    ['task_1','queue_1'],
)
worker.set_task_routes(task_routes)

# Discover tasks in remote files
module_locations = [
    'celery_config.tasks',
]
worker.discover_tasks(module_locations)

if __name__ == '__main__':
    worker.__call__(sys.argv)