# Generated by Django 2.2 on 2019-05-20 22:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('range', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(default=datetime.datetime(2019, 5, 22, 22, 22, 48, 523626, tzinfo=utc))),
                ('wall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrawls.Wall')),
            ],
        ),
    ]
