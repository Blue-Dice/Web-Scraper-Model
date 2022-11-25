from celery import Celery
from decouple import config
import sys

# Location of the celery worker in the project starting from root directory
worker_location = 'worker.celery_worker'

# task that will be assigned designated queue
task_routes = {
    'task_name': {'queue': 'queue_name'}
}

# Broker URL
redis_url = config('REDIS_URL')

# Main Celery worker
celery_worker = Celery(
    'Scraper',
    broker = redis_url,
    backend = redis_url,
)

# Assign task routes to the worker
celery_worker.conf.update({
    'task_routes': task_routes
})

# List of file name where celery tasks are running
celery_task_file = ['tasks']

# Discover celery tasks in different files
celery_worker.autodiscover_tasks(celery_task_file, force=True)

# All the queues assigned to the worker
celery_queues = ''.join([task_routes[key]['queue'] + "," for key in task_routes.keys()])[:-1]

# Celery worker startup sessages
celery_command_error_message = """
    Please specify a valid worker command.
    For more information, use "python worker.py --help"
"""
celery_command_help_message = """
    celery commands for direct execution:
        * Direct execution only works when worker is at the root directory.
        * For direct execution, move to scraper/celery_config/
        [1] celery -A {worker} worker --pool=threads -Q {queues} -l info
        [2] celery -A {worker} purge -Q {queues}
        [3] celery -A {worker} purge -Q {queues} -f

    command line arguments:
        [1] start : to start the celery worker
        [2] purge : to purge all the tasks in the celery queues
        [3] purge -f : to purge all the tasks in the celery queues while skipping the prompt
""".format(worker=worker_location, queues=celery_queues)

worker_start_arguments = ['worker','--pool=threads','-Q',celery_queues,'--loglevel=INFO']
worker_purge_arguments = ['-A',worker_location,'purge','-Q',celery_queues]
worker_force_purge_arguments = ['-A',worker_location,'purge','-Q',celery_queues,'-f']

if __name__ == "__main__":
    try:
        if sys.argv[1] == 'start':
            celery_worker.worker_main(worker_start_arguments)
        elif sys.argv[1] == 'purge':
            if len(sys.argv) > 2 and sys.argv[2] == '-f':
                args = worker_force_purge_arguments
            else:
                args = worker_purge_arguments
            celery_worker.start(args)
        elif sys.argv[1] == '--help':
            print(celery_command_help_message)
        else:
            print(celery_command_error_message)
    except Exception as e:
        print(celery_command_error_message)