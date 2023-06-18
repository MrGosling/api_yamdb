from django.core.management.base import BaseCommand
import csv
from reviews.models import Genre, Category, Title, CustomUser, Review, Comment


class Command(BaseCommand):
    help = 'Загрузка данных в таблицу Titles'

    def handle(self, *args, **options):
        try:
            with open('static/data/titles.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    id = int(row[0])
                    name = row[1]
                    year = int(row[2])
                    category = int(row[3])
                    try:
                        Title.objects.get(
                            id=id,
                            name=name,
                            year=year,
                            category=category
                        )
                    except Title.DoesNotExist:
                        Title.objects.create(
                            id=id,
                            name=name,
                            year=year,
                            category=Category.objects.get(id=category)
                        )
        except FileNotFoundError:
            print('Отсутствует файл titles.csv')
