#!/usr/bin/env bash

cd /opt/bin
gunicorn3 --bind 0.0.0.0:8000 server:app
