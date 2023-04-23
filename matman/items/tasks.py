from datetime import timedelta
from typing import Any

from django.utils.timezone import now
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from celery import shared_task

from .models import Borrow, Item, Comment


User = get_user_model()


def check_if_send_notification(user: User | None) -> bool:
    """
    Check if notification can/should be sent to a certain User.

    Check if:
        - user is not None
        - user has an email address registered
        - user is active

    :param user: User to be checked. Also accepts None value.
    :return: True, if notification should be sent to the given user, else false.
    """

    return all([
        user is not None,
        user.email,
        user.is_active
    ])


@shared_task
def send_item_notifications(item_pk: int, created: bool, editor_pk: int | None):
    item: Item = Item.objects.get(pk=item_pk)
    editor: User = User.objects.get(pk=editor_pk)
    context: dict[str, Any] = {
        'item': item,
        'created': created,
        'editor': editor,
        'site': Site.objects.get_current(),
    }
    from_email: str = settings.DEFAULT_FROM_EMAIL
    subject: str = f'MatMan - Item {item.identifier} {"created" if created else "updated"}'
    notified_users: set[User] = {item.owner, editor}

    for user in notified_users:
        if not check_if_send_notification(user):
            continue
        context['recipient'] = user
        html_message: str = render_to_string('items/mail/item_notification.html', context)
        plain_message: str = strip_tags(html_message)
        mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[user.email],
                       html_message=html_message)


@shared_task
def send_comment_notifications(comment_pk: int, created: bool, editor_pk: int | None):
    comment: Comment = Comment.objects.get(pk=comment_pk)
    editor: User = User.objects.get(pk=editor_pk)
    context: dict[str, Any] = {
        'item': comment.item,
        'comment': comment,
        'created': created,
        'editor': editor,
        'site': Site.objects.get_current(),
    }
    item: Item = comment.item
    from_email: str = settings.DEFAULT_FROM_EMAIL
    subject: str = f'MatMan - Comment on {item.identifier} {"created" if created else "updated"}'
    notified_users: set[User] = {item.owner, editor}
    if item.is_borrowed:
        notified_users.add(item.active_borrow.borrowed_by)

    for user in notified_users:
        if not check_if_send_notification(user):
            continue
        context['recipient'] = user
        html_message: str = render_to_string('items/mail/comment_notification.html', context)
        plain_message: str = strip_tags(html_message)
        mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[user.email],
                       html_message=html_message)


@shared_task
def send_borrow_notifications(borrow_pk: int, created: bool, returned: bool, editor_pk: int | None):
    borrow: Borrow = Borrow.objects.get(pk=borrow_pk)
    editor: User = User.objects.get(pk=editor_pk)
    context: dict[str, Any] = {
        'borrow': borrow,
        'created': created,
        'returned': returned,
        'editor': editor,
        'site': Site.objects.get_current(),
    }
    item: Item = borrow.item
    from_email: str = settings.DEFAULT_FROM_EMAIL
    subject: str = f'MatMan - Borrow for item {item.identifier} updated'
    if created:
        subject = f'MatMan - Item {item.identifier} borrowed'
    elif returned:
        subject = f'MatMan - Item {item.identifier} returned'
    notified_users: set[User] = {item.owner, editor, borrow.borrowed_by}

    for user in notified_users:
        if not check_if_send_notification(user):
            continue
        context['recipient'] = user
        html_message: str = render_to_string('items/mail/borrow_notification.html', context)
        plain_message: str = strip_tags(html_message)
        mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[user.email],
                       html_message=html_message)


@shared_task
def send_reminders():
    today = now().date()
    # yesterday = today - timedelta(days=1)
    subject = 'MatMan - Borrow expiration reminder'
    for user in User.objects.all():
        context = {
            # 'overdue': user.borrows.active.filter(estimated_returndate__lte=yesterday),
            'due': user.borrows.filter(estimated_returndate__lte=today,
                                       returned_at__isnull=True),
            'user': user,
            'site': Site.objects.get_current(),
        }
        if not context['due'].count():
            # Nothing to do, continue with next user
            continue

        html_message: str = render_to_string('items/mail/borrow_reminder.html', context)
        plain_message: str = strip_tags(html_message)
        from_email: str = settings.DEFAULT_FROM_EMAIL
        mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[user.email],
                       html_message=html_message)

