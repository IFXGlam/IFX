# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_bid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('title', models.CharField(max_length=300)),
                ('type1_id', models.CharField(max_length=300)),
            ],
        ),
    ]
