FROM python:3.6-slim

WORKDIR /app
ADD . /app

RUN set -ex;\
    apt-get update; \
    pip install -U pip && \
    pip install -r requirements.txt;

CMD [ "python3", "app.py" ]