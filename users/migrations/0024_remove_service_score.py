# Generated by Django 3.1.6 on 2021-05-03 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_service_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='score',
        ),
    ]