# Generated by Django 3.1.6 on 2021-04-22 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_service_image_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image_couverture',
        ),
    ]
