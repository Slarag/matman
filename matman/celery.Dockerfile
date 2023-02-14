FROM python:latest

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install celery

WDIR /matman/matman

# TBD
# CMD celery -A matman worker -l INFO
