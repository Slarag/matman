# Generated by Django 4.0.5 on 2022-09-04 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matman', '0010_alter_materialpicture_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='material',
            name='contains',
            field=models.ManyToManyField(related_name='contained_in', to='matman.material'),
        ),
        migrations.AddField(
            model_name='material',
            name='short_text',
            field=models.CharField(default='N/A', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='about',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='department',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='materialpicture',
            name='material',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='matman.material'),
        ),
    ]