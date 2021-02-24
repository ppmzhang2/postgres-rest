#!/bin/bash

CPUS=$(getconf _NPROCESSORS_ONLN 2> /dev/null)
LOG_FILE="/app/logs/gunicorn.log"
WORKERS=$((2*CPUS+1))
BIND=0.0.0.0:8000
APP_MODULE=run:app

exec gunicorn $APP_MODULE --bind=$BIND \
  --worker-class=aiohttp.GunicornWebWorker \
  --workers=$WORKERS --log-file="$LOG_FILE"
exec "$@"
