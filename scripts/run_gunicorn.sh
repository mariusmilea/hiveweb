#!/usr/bin/env bash

gunicorn --workers 4 \
	 --worker-class gevent \
     --log-level info \
     --error-logfile server.log \
     --bind 0.0.0.0:8080 run:app