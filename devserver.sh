#!/bin/sh
source .venv/bin/activate
python snipbox/manage.py runserver $PORT
