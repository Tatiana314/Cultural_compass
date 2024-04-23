import logging
import os
import sqlite3

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand

logging.basicConfig(
    level=logging.INFO, format=('%(asctime)s - %(levelname)s - %(message)s')
)

SERIES_NAME = {'category': 'category_id', 'author': 'author_id'}
PATH_TABLE = (
    ('static/data/users.csv', 'users_user'),
    ('static/data/titles.csv', 'reviews_title'),
    ('static/data/category.csv', 'reviews_categorie'),
    ('static/data/genre.csv', 'reviews_genre'),
    ('static/data/genre_title.csv', 'reviews_genretitle'),
    ('static/data/review.csv', 'reviews_review'),
    ('static/data/comments.csv', 'reviews_comment'),
)
MESSAGE = 'Импорт из файла {path} в таблицу {table} осуществлен.'


class Command(BaseCommand):
    """Импорт группы файлов в БД."""

    help = (
        'Импорт данных из файлов: users.csv, titles.csv, category.csv, '
        'genre.csv, genre_title.csv, review.csv, comments.csv в БД'
    )

    def handle(self, *args, **kwargs):
        connection = sqlite3.connect(settings.DATABASES['default']['NAME'])
        for path, table in PATH_TABLE:
            try:
                data = pd.read_csv(
                    os.path.join(settings.BASE_DIR, path), index_col=0
                )
                data.rename(columns=SERIES_NAME).to_sql(
                    table, connection, if_exists="append", index=False
                )
                logging.info(MESSAGE.format(table=table, path=path))
            except Exception as error:
                logging.error(error)
