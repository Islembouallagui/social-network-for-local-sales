# Generated by Django 3.1.6 on 2021-04-03 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_prod_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_business', models.EmailField(max_length=254)),
                ('phone_business', models.IntegerField()),
                ('name_business', models.CharField(max_length=200)),
                ('sector', models.CharField(max_length=200)),
                ('userr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
