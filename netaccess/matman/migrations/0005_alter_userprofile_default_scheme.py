# Generated by Django 4.0.5 on 2022-08-22 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matman', '0004_remove_scheme_id_prefix_scheme_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='default_scheme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='matman.scheme'),
        ),
    ]
