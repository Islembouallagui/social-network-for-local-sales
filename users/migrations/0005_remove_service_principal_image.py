# Generated by Django 3.1.6 on 2021-04-03 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210403_1237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='principal_image',
        ),
    ]