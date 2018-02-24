# Generated by Django 2.0.2 on 2018-02-24 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_auto_20180223_1437'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='linktype',
            options={'ordering': ('priority',)},
        ),
        migrations.AlterField(
            model_name='linktype',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='English description'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='description_he',
            field=models.TextField(blank=True, null=True, verbose_name='Hebrew description'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='for_movies',
            field=models.BooleanField(verbose_name='for movies'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='for_people',
            field=models.BooleanField(verbose_name='for people'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='priority',
            field=models.IntegerField(default=100, verbose_name='priority'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='template',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='template'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='title_en',
            field=models.CharField(max_length=300, verbose_name='English title'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='title_he',
            field=models.CharField(max_length=300, verbose_name='Hebrew title'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='title_required',
            field=models.BooleanField(verbose_name='title required'),
        ),
        migrations.AlterField(
            model_name='linktype',
            name='wikidata_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='wikidata id'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='editing_comment',
            field=models.TextField(blank=True, null=True, verbose_name='editing comment'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='language',
            field=models.IntegerField(blank=True, choices=[(1, 'Hebrew'), (2, 'English')], null=True, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='limit_to_language',
            field=models.BooleanField(default=False, verbose_name='limit to this language'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='notes_en',
            field=models.TextField(blank=True, null=True, verbose_name='notes in English'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='notes_he',
            field=models.TextField(blank=True, null=True, verbose_name='notes in Hebrew'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='title_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='English title'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='title_he',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Hebrew title'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movielinks', to='links.LinkType', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='movielink',
            name='value',
            field=models.CharField(max_length=400, verbose_name='value or URL'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='editing_comment',
            field=models.TextField(blank=True, null=True, verbose_name='editing comment'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='language',
            field=models.IntegerField(blank=True, choices=[(1, 'Hebrew'), (2, 'English')], null=True, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='limit_to_language',
            field=models.BooleanField(default=False, verbose_name='limit to this language'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='notes_en',
            field=models.TextField(blank=True, null=True, verbose_name='notes in English'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='notes_he',
            field=models.TextField(blank=True, null=True, verbose_name='notes in Hebrew'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='title_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='English title'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='title_he',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Hebrew title'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='personlinks', to='links.LinkType', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='personlink',
            name='value',
            field=models.CharField(max_length=400, verbose_name='value or URL'),
        ),
    ]
