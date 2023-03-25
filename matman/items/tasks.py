from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from celery import shared_task
from celery.schedules import crontab

from .models import Borrow, Item

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # # Calls test('hello') every 10 seconds.
#     # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#     #
#     # # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=9, minute=0),
#         send_reminders.s(),
#     )


@shared_task
def notify_borrow_created(borrow):
    pass


@shared_task
def notify_borrow_updated(borrow):
    pass


@shared_task
def notify_borrow_closed(borrow):
    pass


@shared_task
def send_reminders():
    for borrow in Borrow.due_soon.all():
        subject = 'MatMan - Borrow expiration reminder'
        html_message = strip_tags(render_to_string('items/mail/borrow_reminder.html', {'borrow': borrow}))
        plain_message = strip_tags(html_message)
        from_email = f'From {settings.DEFAULT_FROM_EMAIL}'
        to = borrow.borrowed_by.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

