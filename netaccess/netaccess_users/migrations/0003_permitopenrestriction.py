# Generated by Django 4.0.5 on 2022-06-24 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netaccess_users', '0002_sshpubkey_comment_sshpubkey_date_added_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermitOpenRestriction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=100)),
                ('port', models.PositiveIntegerField(blank=True)),
                ('pubkey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permit_open', to='netaccess_users.sshpubkey')),
            ],
        ),
    ]