FROM python:latest

# ARG DJANGO_SUPERUSER_PASSWORD
# ARG DJANGO_SUPERUSER_USERNAME
# ARG DJANGO_SUPERUSER_EMAIL

# RUN apt install git caddy openssh-server
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install daphne

WDIR /matman/matman

# RUN python3 ./manage.py makemigrations
RUN python3 ./manage.py migrate
RUN python3 ./manage.py collectstatic
# RUN python3 ./manage.py createsuperuser --noinput

CMD daphne matman.asgi:application --port 8000 --proxy-headers
