# Generated by Django 2.2.1 on 2019-05-24 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrawls', '0002_auto_20190520_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wall',
            name='address',
        ),
        migrations.RemoveField(
            model_name='wall',
            name='range',
        ),
    ]