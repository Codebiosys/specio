from celery import Celery


app = Celery(
    'forrest',
    broker='redis://queue/',
    backend='redis://queue/',
 )

app.conf.task_serializer = 'json'
app.conf.worker_hijack_root_logger = False
app.conf.worker_redirect_stdouts_level = 'debug'
