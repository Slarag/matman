from datetime import timedelta

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

@shared_task
def send_item_notifications(item_pk: int, created: bool, editor_pk: int | None):
    item = Item.objects.get(pk=item_pk)
    editor = User.objects.get(pk=editor_pk)
    context = {
        'item': item,
        'created': created,
        'editor': editor,
        'site': Site.objects.get_current(),
    }
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = f'MatMan - Item {item.identifier} {"created" if created else "updated"}'

    if item.owner is not None and item.owner.email:
        # Send notification to owner
        context['recipient'] = item.owner
        html_message = render_to_string('items/mail/item_notification.html', context)
        plain_message = strip_tags(html_message)
        to = item.owner.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    if editor is not None and editor != item.owner and editor.email:
        # Send notification to creator
        context['recipient'] = editor
        html_message = render_to_string('items/mail/item_notification.html', context)
        plain_message = strip_tags(html_message)
        to = editor.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


@shared_task
def send_comment_notifications(comment_pk: int, created: bool, editor_pk: int | None):
    comment = Comment.objects.get(pk=comment_pk)
    editor = User.objects.get(pk=editor_pk)
    context = {
        'item': comment.item,
        'comment': comment,
        'created': created,
        'editor': editor,
        'site': Site.objects.get_current(),
    }
    item = comment.item
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = f'MatMan - Comment on {item.identifier} {"created" if created else "updated"}'

    if item.owner is not None and item.owner.email:
        # Send notification to owner
        context['recipient'] = item.owner
        html_message = render_to_string('items/mail/comment_notification.html', context)
        plain_message = strip_tags(html_message)
        to = item.owner.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    if editor is not None and editor != item.owner and editor.email:
        # Send notification to creator
        context['recipient'] = editor
        html_message = render_to_string('items/mail/comment_notification.html', context)
        plain_message = strip_tags(html_message)
        to = editor.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    if item.is_borrowed:
        borrow = item.active_borrow
        borrowed_by = borrow.borrowed_by
        if borrowed_by not in (item.owner, editor) and borrowed_by.email:
            # Also send email to person who has currently borrowed the item
            context['recipient'] = borrowed_by
            html_message = render_to_string('items/mail/comment_notification.html', context)
            plain_message = strip_tags(html_message)
            to = borrowed_by.email
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


@shared_task
def send_borrow_notifications(borrow_pk: int, created: bool, returned: bool, editor_pk: int | None):
    borrow = Borrow.objects.get(pk=borrow_pk)
    editor = User.objects.get(pk=editor_pk)
    context = {
        'borrow': borrow,
        'created': created,
        'returned': returned,
        'editor': editor,
        'site': Site.objects.get_current(),
    }
    item = borrow.item
    from_email = settings.DEFAULT_FROM_EMAIL
    if created:
        subject = f'MatMan - Item {item.identifier} borrowed'
    elif returned:
        subject = f'MatMan - Item {item.identifier} returned'
    else:
        subject = f'MatMan - Borrow for item {item.identifier} updated'

    if item.owner is not None and item.owner.email:
        # Send notification to owner
        context['recipient'] = item.owner
        html_message = render_to_string('items/mail/borrow_notification.html', context)
        plain_message = strip_tags(html_message)
        to = item.owner.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    if editor is not None and editor != item.owner and editor.email:
        # Send notification to creator
        context['recipient'] = editor
        html_message = render_to_string('items/mail/borrow_notification.html', context)
        plain_message = strip_tags(html_message)
        to = editor.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    if borrow.borrowed_by not in (editor, item.owner) and borrow.borrowed_by.email:
        # Send notification to creator
        context['recipient'] = borrow.borrowed_by
        html_message = render_to_string('items/mail/borrow_notification.html', context)
        plain_message = strip_tags(html_message)
        to = borrow.borrowed_by.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


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

        html_message = render_to_string('items/mail/borrow_reminder.html', context)
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to = user.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

