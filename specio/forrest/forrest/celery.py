from celery import Celery


app = Celery(
    'forrest',
    broker='redis://queue/',
    backend='redis://queue/',
 )

app.conf.task_serializer = 'json'
app.conf.worker_hijack_root_logger = False
app.conf.worker_redirect_stdouts_level = 'debug'


# BEGIN DEBUG CELERY SETTINGS
#
app.conf.task_always_eager = True
app.conf.task_eager_propagates = True
#
# END CELERY DEBUG SETTINGS
