import pandas as pd
import random
import silly
import numpy as np

# TODO: use tqdm for progress bar

from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = "Import movies."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str)

    def handle(self, f, **options):
        df = pd.read_csv(f, delimiter='\t')
        c = len(df)
        for i, row in df.iterrows():
            if Movie.objects.filter(bid=row.bid).exists():
                continue

            if i % 200 == 0:
                print(i, c, row.bid, row.title)

            o = Movie()
            o.bid = row.bid
            o.title = row.title
            o.year = None if np.isnan(row.year) else row.year
            o.lang = row.lang
            o.full_clean()
            o.save()
