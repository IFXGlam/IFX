# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-06 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', models.CharField(max_length=300, unique=True)),
                ('title', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField(unique=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('title_he', models.CharField(blank=True, max_length=300, null=True)),
                ('title_en', models.CharField(blank=True, max_length=300, null=True)),
                ('summary_he', models.TextField(blank=True, null=True)),
                ('summary_en', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovieTagField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Field')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=300)),
                ('type_id', models.CharField(blank=True, max_length=300, null=True)),
                ('lang', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='movietagfield',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Tag'),
        ),
    ]
