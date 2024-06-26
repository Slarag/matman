# Generated by Django 4.1.7 on 2023-03-18 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.SlugField(editable=False, unique=True, verbose_name='ID')),
                ('short_text', models.CharField(blank=True, max_length=100, verbose_name='Short Text')),
                ('serial_number', models.CharField(blank=True, max_length=30, verbose_name='Serial Number')),
                ('revision', models.CharField(blank=True, max_length=30, verbose_name='Revision/Version')),
                ('part_number', models.CharField(blank=True, max_length=30, verbose_name='Part Number')),
                ('manufacturer', models.CharField(blank=True, max_length=30, verbose_name='Manufacturer')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='Location')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last edited')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_items', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('prefix', models.CharField(blank=True, default='', max_length=10)),
                ('numlen', models.PositiveIntegerField(default=6)),
                ('postfix', models.CharField(blank=True, default='', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('_id_counter', models.PositiveBigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(blank=True, max_length=30)),
                ('about', models.TextField(blank=True)),
                ('bookmarks', models.ManyToManyField(blank=True, related_name='bookmarked_by', to='items.item')),
                ('default_scheme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.scheme')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='Description')),
                ('file', models.ImageField(upload_to='pictures/', verbose_name='File')),
                ('item', simple_history.models.HistoricForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='items.item', verbose_name='Item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='scheme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.scheme'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='HistoricalScheme',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('prefix', models.CharField(blank=True, default='', max_length=10)),
                ('numlen', models.PositiveIntegerField(default=6)),
                ('postfix', models.CharField(blank=True, default='', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical scheme',
                'verbose_name_plural': 'historical schemes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalItemPicture',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='Description')),
                ('file', models.TextField(max_length=100, verbose_name='File')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item', simple_history.models.HistoricForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='items.item', verbose_name='Item')),
            ],
            options={
                'verbose_name': 'historical item picture',
                'verbose_name_plural': 'historical item pictures',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalItem',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('identifier', models.SlugField(editable=False, verbose_name='ID')),
                ('short_text', models.CharField(blank=True, max_length=100, verbose_name='Short Text')),
                ('serial_number', models.CharField(blank=True, max_length=30, verbose_name='Serial Number')),
                ('revision', models.CharField(blank=True, max_length=30, verbose_name='Revision/Version')),
                ('part_number', models.CharField(blank=True, max_length=30, verbose_name='Part Number')),
                ('manufacturer', models.CharField(blank=True, max_length=30, verbose_name='Manufacturer')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='Location')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('creation_date', models.DateTimeField(blank=True, editable=False, verbose_name='Creation Date')),
                ('last_updated', models.DateTimeField(blank=True, editable=False, verbose_name='Last edited')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('scheme', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='items.scheme')),
            ],
            options={
                'verbose_name': 'historical item',
                'verbose_name_plural': 'historical items',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalComment',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(blank=True, editable=False)),
                ('text', models.TextField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='items.item')),
            ],
            options={
                'verbose_name': 'historical comment',
                'verbose_name_plural': 'historical comments',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalBorrow',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('borrowed_at', models.DateTimeField(blank=True, editable=False, verbose_name='Borrowed at')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('usage_location', models.CharField(blank=True, max_length=100, verbose_name='Usage Location')),
                ('estimated_returndate', models.DateField(blank=True, null=True, verbose_name='Estimated return date')),
                ('returned_at', models.DateTimeField(blank=True, null=True, verbose_name='Returned at')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('borrowed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Borrowed by')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='items.item', verbose_name='Item')),
                ('returned_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Returned by')),
            ],
            options={
                'verbose_name': 'historical borrow',
                'verbose_name_plural': 'historical borrows',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='items.item')),
            ],
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_at', models.DateTimeField(auto_now_add=True, verbose_name='Borrowed at')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('usage_location', models.CharField(blank=True, max_length=100, verbose_name='Usage Location')),
                ('estimated_returndate', models.DateField(blank=True, null=True, verbose_name='Estimated return date')),
                ('returned_at', models.DateTimeField(blank=True, null=True, verbose_name='Returned at')),
                ('borrowed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrows', to=settings.AUTH_USER_MODEL, verbose_name='Borrowed by')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrows', to='items.item', verbose_name='Item')),
                ('returned_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrows_returned', to=settings.AUTH_USER_MODEL, verbose_name='Returned by')),
            ],
        ),
    ]
