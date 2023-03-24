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

## Project Status

This project is still a WIP (Work In Progress).

## Quickstart

- Clone repository
- Adapt `matman/matman/settings/production.py` to fit your needs
  - *IMPORTANT:* Change `DJANGO_SECRET_KEY` variable to a unique value! See [Django documentation](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY) for details
- Run `docker compose build` to build the container images
- Start the application by running `docker compose up -d`
- To create an initial superusers run `docker exec -it matman-daphne-1 python manage.py createsuperuser`
