# Generated by Django 3.1.6 on 2021-04-08 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210406_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='principal_image',
            field=models.FileField(blank=True, upload_to='images/'),
        ),
    ]