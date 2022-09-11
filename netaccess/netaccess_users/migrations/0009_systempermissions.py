# Generated by Django 4.0.5 on 2022-06-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netaccess_users', '0008_alter_permitopenrestriction_port_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('can_use_ssh', 'Allow SSH access'), ('can_use_samba', 'Allow Samba access')),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]
