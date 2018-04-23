# Generated by Django 2.0.2 on 2018-02-27 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0005_move_generic_links'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movielink',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='movielink',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='movielink',
            name='type',
        ),
        migrations.AlterUniqueTogether(
            name='personlink',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='personlink',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='personlink',
            name='type',
        ),
        migrations.DeleteModel(
            name='MovieLink',
        ),
        migrations.DeleteModel(
            name='PersonLink',
        ),
    ]