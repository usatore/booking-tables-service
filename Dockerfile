FROM python:3.13.0-slim

WORKDIR /tgliker

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .