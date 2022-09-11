# Generated by Django 4.0.5 on 2022-08-22 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matman', '0003_rename_department_scheme_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheme',
            name='id_prefix',
        ),
        migrations.AddField(
            model_name='scheme',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='scheme',
            name='numlen',
            field=models.PositiveIntegerField(default=6),
        ),
        migrations.AddField(
            model_name='scheme',
            name='postfix',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='scheme',
            name='prefix',
            field=models.CharField(default='ID', max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
