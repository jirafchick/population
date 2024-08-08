FROM python:3.12.2-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY . /app

WORKDIR /app

RUN apk update && apk add --no-cache curl

RUN pip install --upgrade pip && pip install .
