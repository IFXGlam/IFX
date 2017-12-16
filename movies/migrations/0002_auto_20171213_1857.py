# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie_tag_field',
            name='field',
        ),
        migrations.AddField(
            model_name='movie_tag_field',
            name='field',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movies.Field'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='movie_tag_field',
            name='movie',
        ),
        migrations.AddField(
            model_name='movie_tag_field',
            name='movie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movies.Movie'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='movie_tag_field',
            name='tag',
        ),
        migrations.AddField(
            model_name='movie_tag_field',
            name='tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movies.Tag'),
            preserve_default=False,
        ),
    ]
