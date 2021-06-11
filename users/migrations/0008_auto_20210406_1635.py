# Generated by Django 3.1.6 on 2021-04-06 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210406_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='prod',
            name='Latitude',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='prod',
            name='Longitude',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='Latitude',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='Longitude',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
