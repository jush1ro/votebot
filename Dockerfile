FROM python:3.8

ENV BOT_TOKEN=""
ENV DATABASE_FILE="/app/data/data.db"

COPY requirements.txt /app/
RUN python -m pip install -r /app/requirements.txt
RUN apt-get update && apt-get install sqlite3

COPY ./src/ /app/src/
VOLUME ./data/ /app/data/
RUN sqlite3 /app/data/data.db < /app/src/createdb.sql

# TODO Fix volume mounting

WORKDIR /app/

ENTRYPOINT python /app/src/main.py