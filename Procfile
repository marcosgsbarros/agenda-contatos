#web: gunicorn --pythonpath . agenda.wsgi --bind 0.0.0.0:$PORT --workers 2 --chdir /app --log-level=debug
web: gunicorn agenda.wsgi --bind 0.0.0.0:$PORT --workers 2 --log-level=debug --access-logfile -
