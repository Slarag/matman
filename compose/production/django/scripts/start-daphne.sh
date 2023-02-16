#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate
python manage.py collectstatic --noinput
daphne matman.asgi:application --bind 0.0.0.0 --port 8000 --proxy-headers