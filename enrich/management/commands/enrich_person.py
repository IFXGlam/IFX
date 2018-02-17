import random
from tqdm import tqdm
import silly
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from movies.models import Person, models
from enrich.models import Identity

class Command(BaseCommand):
    help = "Enrich person"

    def add_arguments(self, parser):
        parser.add_argument('n', type=int)
        parser.add_argument(
            'type',
            type=str,
        )

        parser.add_argument(
            '--readonly',
            action='store_true',
            dest='readonly',
            help='Parse it without saving to database',
        )

    def handle(self, n, **options):
        person_id = 0
        progress = tqdm(total=n)
        for i in range(n):
            try:
                person = Person.objects.order_by('?').first()
                print('Person = ' + str(person))
            except models.ObjectDoesNotExist:
                print('Person not found')

            if person:
                ct = ContentType.objects.get_for_model(person)
                o = Identity.objects.filter(content_type=ct, object_id=person.id).first()
            if o:
                print('Found identity by person, id={}'.format(o.object_id))
            else:
                o = Identity.objects.create(entity=person, source_type=Identity.wikipedia)
                print('Identity created with person, id={}'.format(o.object_id))

                o.get_wikipedia_info()

                o.get_viaf_info()

            if not options['readonly']:
                o.save()
            progress.update(1)

        progress.close()