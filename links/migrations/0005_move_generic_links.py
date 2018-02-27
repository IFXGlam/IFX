# Generated by Django 2.0.2 on 2018-02-26 22:59

from django.db import migrations


def forwards_func(apps, schema_editor):
    Link = apps.get_model("links", "Link")
    MovieLink = apps.get_model("links", "MovieLink")
    PersonLink = apps.get_model("links", "PersonLink")
    ContentType = apps.get_model("contenttypes", "ContentType")
    movie_ct = ContentType.objects.get(app_label='movies', model='movie')
    person_ct = ContentType.objects.get(app_label='people', model='person')

    db_alias = schema_editor.connection.alias

    def do(model, ct):
        for o in model.objects.using(db_alias).all():
            d = o.__dict__.copy()
            del d['_state']
            d['content_type'] = ct
            d['object_id'] = d.pop('parent_id')
            Link.objects.create(**d)

    do(MovieLink, movie_ct)
    do(PersonLink, person_ct)


class Migration(migrations.Migration):
    dependencies = [
        ('links', '0004_link'),
    ]

    operations = [
        migrations.RunPython(forwards_func)
    ]
