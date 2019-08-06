FROM python:3.6-slim

WORKDIR /app
ADD requirements.txt /app

RUN set -ex;\
    apt-get update; \
    pip install -U pip && \
    pip install -r requirements.txt;

ADD . /app
CMD [ "python3", "app.py" ]