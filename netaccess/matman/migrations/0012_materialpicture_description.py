# Generated by Django 4.0.5 on 2022-09-04 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matman', '0011_borrow_notes_material_contains_material_short_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialpicture',
            name='description',
            field=models.CharField(default='description', max_length=50),
            preserve_default=False,
        ),
    ]