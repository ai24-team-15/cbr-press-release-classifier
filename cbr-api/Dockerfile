FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./cbr-api/

RUN pip3 install -r cbr-api/requirements.txt

COPY . ./cbr-api
