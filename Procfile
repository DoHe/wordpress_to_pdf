web: gunicorn server.app:app --log-file -
worker: celery -A server.tasks worker