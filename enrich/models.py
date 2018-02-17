import wikipedia

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

from django.db import models

from movies.models import Person
from .api import ViafAPI


class Identity(models.Model):
    """
    # Identity
    # - entity = GenericFK (-> Person ->Movie)
    # - source (choices = WIKIDATA, WIKIPEDIA, VIAF,)
    # - vendor_id ("X1234" "https://hw.wikipedia.org/HAIM=TOPUL"
    # - status: NEW, ACCEPTED, REJECTED, UNDER_DISCUSSION
    # - notes:
    # - score???: automatic probabilty (0.4 for name + 0.5 for matching role in movie)
    """
    wikidata = 'WIKIDATA'
    wikipedia = 'WIKIPEDIA'
    viaf = 'VIAF'

    SOURCE_TYPE_CHOICES = (
        (wikidata, 'WIKIDATA'),
        (wikipedia, 'WIKIPEDIA'),
        (viaf, 'VAIF'),
    )
    source_type = models.CharField(max_length=300, choices=SOURCE_TYPE_CHOICES, default='VIAF')
    source_value = models.CharField(max_length=300, null=True, blank=True)

    STATUS_CHOICES = (
        ('NEW', 'NEW'),
        ('ACCEPTED', 'ACCEPTED'),
        ('REJECTED', 'REJECTED'),
        ('UNDER_DISCUSSION', 'UNDER_DISCUSSION'),
    )
    status = models.CharField(max_length=300, choices=STATUS_CHOICES, default='NEW')

    notes = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    # Below the mandatory fields for generic relation

    # TODO: implement GenericForiegnKey:
    # https://axiacore.com/blog/how-use-genericforeignkey-django/
    # https://docs.djangoproject.com/en/2.0/ref/contrib/contenttypes/
    limit = models.Q(app_label='movies', model='person') | \
        models.Q(app_label='movies', model='movie')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('content person'),
        limit_choices_to=limit,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('related object'),
        null=True,
    )
    entity = GenericForeignKey('content_type', 'object_id')
    # content_object = GenericForeignKey()

    # https://en.wikipedia.org/w/index.php?search=Edward+Dmytryk
    # http://viaf.org/viaf/search?query=local.personalNames+all+%22Edward%20Dmytryk%22&sortKeys=holdingscount&recordSchema=BriefVIAF
    URIs = {
        wikidata: 'https://en.wikipedia.org/w/index.php?search={}',
        wikipedia: 'https://www.wikimedia.org/',
        viaf: 'http://viaf.org/viaf/search?query=local.personalNames+all+"{}"&sortKeys=holdingscount&recordSchema=BriefVIAF',
    }

    def enrich_object(self):
        print(self.source_type)
        uri = self.URIs[self.source_type]
        print(uri)

    def get_wikipedia_info(self):
        # https://pypi.python.org/pypi/wikipedia
        try:
            # TODO: movie support
            p = Person.objects.get(pk=self.object_id)
            name = p.name_en
            try:
                url = wikipedia.page(name).url
                print(url)
            except wikipedia.exceptions.DisambiguationError as e:
                print(e.options)
        except:
            print('Not found, Id={}'.format(self.object_id))

    def get_viaf_info(self):
        # https://www.viaf.org/viaf
        try:
            # TODO: movie support
            p = Person.objects.get(pk=self.object_id)
            name = p.name_en
            # remove me
            name = 'Edward Dmytryk'
            try:
                viaf = ViafAPI()
                items = viaf.find_person(name)
                # print(items)
                counter = 1
                for item in items:
                    print('item #{}'.format(counter))
                    print('uri={}'.format(item.uri))
                    print('viaf_id={}'.format(item.viaf_id))
                    print('nametype={}'.format(item.nametype))
                    print('label={}'.format(item.label))
                    counter += 1
            except Exception as e:
                print(e.options)
        except:
            print('Not found, Id={}'.format(self.object_id))
