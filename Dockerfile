FROM python:3.11-alpine

RUN apk add bash

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY OpenShow .

RUN apk add ffmpeg

ARG OPENSHOW_DEBUG='False'
ARG OPENSHOW_STATIC_ROOT='/static-root'
ARG OPENSHOW_MEDIA_ROOT='/media-root'
ARG OPENSHOW_ALLOWED_HOSTS='0.0.0.0'
ARG OPENSHOW_SQLITE3_PATH='/db.sqlite3'
ARG DJANGO_SETTINGS_MODULE='OpenShow.settings.prod'

ENV OPENSHOW_DEBUG=${OPENSHOW_DEBUG}
ENV OPENSHOW_SECRET_KEY=${OPENSHOW_SECRET_KEY}
ENV OPENSHOW_STATIC_ROOT=${OPENSHOW_STATIC_ROOT}
ENV OPENSHOW_MEDIA_ROOT=${OPENSHOW_MEDIA_ROOT}
ENV OPENSHOW_ALLOWED_HOSTS=${OPENSHOW_ALLOWED_HOSTS}
ENV OPENSHOW_SQLITE3_PATH=${OPENSHOW_SQLITE3_PATH}
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}

EXPOSE 8000/

ENTRYPOINT echo Migrating... \
    && python manage.py migrate --no-input \
    && python manage.py collectstatic --no-input \
    && python -m uvicorn --host 0.0.0.0 --port 8000 OpenShow.asgi:application
