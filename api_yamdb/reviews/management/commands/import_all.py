from django.core.management.base import BaseCommand
import csv
from reviews.models import Genre, Category, Title, CustomUser, Review, Comment
from reviews.management.commands.import_csv import import_genre


class Command(BaseCommand):
    help = 'Загрузка данных из определённых csv файлов'

    def handle(self, *args, **options):
        import_genre()