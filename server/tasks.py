from celery import Celery

from wordpress_to_pdf import buffer_to_buffer

CELERY = Celery('tasks')
CELERY.config_from_object('server.celery_config')


@CELERY.task
def convert_blog(xml):
    return buffer_to_buffer(xml, '#00CED1', '"Georgia", serif', 450, [])
