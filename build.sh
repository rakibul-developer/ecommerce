#!/usr/bin/env bash
set -o errexit

pip install -r requirements/requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [[ $CREATE_SUPERUSER == "True" ]]; then
    python manage.py createsuperuser --noinput || true
fi