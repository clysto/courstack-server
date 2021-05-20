#!/usr/bin/env bash

cd /code || exit
alembic upgrade head
uvicorn app:app --host 0.0.0.0 --port 8000
