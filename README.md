# Matman - a simple Material/Item Manager

Tired of your colleagues borrowing stuff from you and never returning it? Or are you a busy person who borrows stuff from colleagues and forgets to return it? Or maybe you are a little bit of both at the same time? Or your colleagues are?

Or do you want to keep track of your test equipment and refer to it in reports/documents using a short but unique ID?

**Matman is the solution for you!** It's a lightweight django-based webapp which offers the following:
- Custom unique IDs for your items/material
- Tagging support
- Item metadata like serial number, part number, revision, etc.
- Item tracking (borrow and return items)
- Search items by applying filters
- Add pictures of your material

## LDAP Integration

Support for LDAP integrations is planned, but not yet implemented/tested.
This allows your employees/colleagues to log in with their company credentials without having to register separately.

## Project Status

This project is still a WIP (Work In Progress).

## Quickstart

- Clone repository
- Generate a new secret key and set it as environment variable: `export DJANGO_SECRET_KEY="..."`, see [Django documentation](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY) for details
- Setup database: `python ./manage.py makemigrations && python ./manage.py migrate`
- Create superuser: `python ./manage.py createsuperuser && python ./manage.py loaddata fixture_initial.yaml`

## Serve app with Caddy and Daphne (Example)

Serve Django app with Daphne: `daphne matman.asgi:application --port 8000 --proxy-headers`

Use Caddy as proxy and for serving static and media files:
```
# /etc/caddy/Caddyfile
https://mydomain:443 {
    @static {
        path /static/*
    }
    @media {
        path /static/*
    }
    @daphne {
        path *
        not path /static/*
        not path /media/*
    }
    reverse_proxy @daphne localhost:8000
    file_server @static {
        root PROJECTDIR/files/static/
    }
    file_server @media {
        root PROJECTDIR/files/static/
    }
}
```