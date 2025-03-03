FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt ./cbr-api/

RUN pip3 install --no-cache-dir -r cbr-api/requirements.txt

COPY . ./cbr-api
