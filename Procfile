web: gunicorn agenda.wsgi --bind 0.0.0.0:$PORT --workers 2 --preload-app --chdir /app --static-url /static/ --log-level=debug
