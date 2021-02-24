FROM python:3.8.5-buster

LABEL maintainer="Meng <ztz2000@gmail.com>"

COPY . /app

WORKDIR /app

RUN rm -rf /var/log/supervisord \
    && mkdir -p /var/log/supervisord \
    && pip install -r /app/requirements.txt

CMD ["supervisord", "-c", "/app/etc/wsgi/supervisord.conf"]
