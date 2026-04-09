FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# O comando abaixo é a "alma" do seu deploy agora:
CMD python manage.py migrate --noinput; python criar_usuario.py; gunicorn mecajato.wsgi --bind 0.0.0.0:$PORT --log-file -