#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate
python manage.py collectstatic
daphne matman.asgi:application --port 8000 --proxy-headers