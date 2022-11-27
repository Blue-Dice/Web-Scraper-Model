from worker import worker

@worker.app.task(name='task_1')
def add(a,b):
    print(f"=========================> {a+b}")