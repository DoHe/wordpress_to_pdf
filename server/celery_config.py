import os

BROKER_URL = os.getenv('CLOUDAMQP_URL', 'amqp://localhost')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost')

CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
