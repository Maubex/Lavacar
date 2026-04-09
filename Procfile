release: python manage.py migrate --noinput && python seed.py
web: gunicorn mecajato.wsgi