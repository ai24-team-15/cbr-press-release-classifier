FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt ./cbr-ui/

RUN pip3 install --no-cache-dir -r cbr-ui/requirements.txt

COPY . ./cbr-ui
