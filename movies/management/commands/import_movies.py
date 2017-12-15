import pandas as pd
import numpy as np
from tqdm import tqdm

from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = "Import movies."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str,
                            help='file path to import from')

        parser.add_argument(
            '--readonly',
            action='store_true',
            dest='readonly',
            help='Parse it without saving to database',
        )

        parser.add_argument(
            '--json',
            action = 'store_true',
            dest = 'json',
            help = 'input is json file',
        )

    def handle(self, f, **options):
        if options['json']:
            return self.handle_json(f, **options)

        df = pd.read_csv(f, delimiter='\t')

        progress = tqdm(total=len(df))

        for i, row in df.iterrows():
            if Movie.objects.filter(bid=row.bid).exists():
                continue

            o = Movie()
            o.bid = row.bid
            o.title = row.title
            o.year = None if np.isnan(row.year) else row.year
            o.lang = row.lang
            o.full_clean()

            if not options['readonly']:
                o.save()
            progress.update(1)

        progress.close()

    def handle_json(self, f, **options):
        df = pd.read_json(f)

        progress = tqdm(total=len(df))

        for i, row in df.iterrows():
            if Movie.objects.filter(bid=row.fields['bid']).exists():
                continue

            o = Movie()
            o.bid = row.fields['bid']
            o.title = row.fields['title']
            o.year = None if np.isnan(row.fields['year']) else row.fields['year']
            o.lang = row.fields['lang']
            o.full_clean()

            if not options['readonly']:
                o.save()
            progress.update(1)

        progress.close()
