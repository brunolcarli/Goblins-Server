FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app

RUN apk add --update mariadb-dev
RUN apk add --no-cache \
            --virtual \
            .build-deps \
            python3-dev \
            build-base \
            linux-headers \
            gcc


COPY game_server/requirements/common.txt .
COPY game_server/requirements/production.txt .
RUN pip3 install -r production.txt

COPY . .

ENV NAME game_server