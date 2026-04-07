release: python manage.py migrate --noinput && python manage.py createsuperuser --noinput
web: python manage.py migrate --noinput && gunicorn mecajato.wsgi