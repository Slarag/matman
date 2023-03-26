from datetime import timedelta

from django.utils.timezone import now
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

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
    User = get_user_model()
    today = now().date()
    # yesterday = today - timedelta(days=1)
    subject = 'MatMan - Borrow expiration reminder'
    for user in User.objects.all():
        context = {
            # 'overdue': user.borrows.active.filter(estimated_returndate__lte=yesterday),
            'due': user.borrows.filter(estimated_returndate__lte=today,
                                       returned_at__isnull=True),
            'user': user,
            'site': get_current_site(),
        }
        if not context['due'].count():
            # Nothing to do, continue with next user
            continue

        html_message = render_to_string('items/mail/borrow_reminder.html', context)
        plain_message = strip_tags(html_message)
        from_email = f'From {settings.DEFAULT_FROM_EMAIL}'
        to = user.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

