# Generated by Django 4.1.7 on 2023-03-25 10:29

from django.db import migrations
from django_celery_beat.models import CrontabSchedule, PeriodicTask





def apply_migration(apps, schema_editor):
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='9',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )
    PeriodicTask.objects.create(
        crontab=schedule,
        name='Send reminders',
        task='items.tasks.send_reminders',
        description='Send out daily reminders to users about due borrows'
    )


def revert_migration(apps, schema_editor):
    PeriodicTask.objects.filter(name='Send reminders').delete()
    CrontabSchedule.objects.filter(
        minute='0',
        hour='9',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_add_scheme_admins_group'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]
