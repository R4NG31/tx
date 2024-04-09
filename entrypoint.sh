#!/bin/bash
echo 'Runnig collectstatic......'
python manage.py collectstatic --no-input --settings=core.settings

echo 'Applying migrations...'
python manage.py makemigrations --settings=core.settings
python manage.py migrate --settings=core.settings

#echo 'Runnig Server...'
gunicorn --env DJANGO_SETTINGS_MODULE=core.settings core.wsgi:application --bind 0.0.0.0:8449 --workers 3