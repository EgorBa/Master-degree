FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app
RUN apt-get update -y && apt-get install -y libpq gcc
RUN pip install -r requirements.txt