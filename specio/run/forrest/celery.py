from celery import Celery


app = Celery(
    'run',
    broker='redis://queue/',
    backend='redis://queue/',
    imports=(
        'run.forrest.tasks',
    ),
 )

app.conf.task_serializer = 'json'
