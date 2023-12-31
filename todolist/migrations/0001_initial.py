# Generated by Django 4.2.5 on 2023-10-10 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('user', models.ForeignKey(blank=True, null=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table_comment': 'Available Projects',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('due_date_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.project')),
            ],
            options={
                'db_table_comment': 'Available Tasks',
                'ordering': ['-created_at'],
            },
        ),
    ]
