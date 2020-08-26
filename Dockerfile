FROM python:3.8

COPY requirements.txt /app/
RUN python -m pip install -r /app/requirements.txt
RUN apt-get update && apt-get install sqlite3

WORKDIR /app/

ADD ./src/ /app/src/

ENTRYPOINT sqlite3 /app/data/data.db < /app/src/createdb.sql && python /app/src/main.py
# TODO Write shell script