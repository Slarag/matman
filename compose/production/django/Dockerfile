FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN python -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN python -m pip install -r /requirements.txt

COPY ./compose/production/django/scripts/* /
RUN chmod +x /*.sh

RUN mkdir /files/
WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
