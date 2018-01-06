BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost'

CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
