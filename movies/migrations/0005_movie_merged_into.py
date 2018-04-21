# Generated by Django 2.0.4 on 2018-04-21 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20180420_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='merged_into',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='movies.Movie'),
        ),
    ]
