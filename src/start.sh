#!/bin/bash

sqlite3 /app/data/data.db < /app/src/createdb.sql
python /app/src/main.py