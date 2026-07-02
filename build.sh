#!/usr/bin/env bash
# Exit on error
set -o errexit

python -m pip install -r requirements.txt

# Run collectstatic
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
