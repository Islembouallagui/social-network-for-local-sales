# Generated by Django 3.1.6 on 2021-04-13 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_service_adress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prod',
            name='name_business',
        ),
    ]
