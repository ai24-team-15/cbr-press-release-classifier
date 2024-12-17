FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./cbr-ui/

RUN pip3 install -r cbr-ui/requirements.txt

COPY . ./cbr-ui
