from django.core.management.base import BaseCommand
import csv
from reviews.models import Genre, Category, Title, CustomUser, Review, Comment
from reviews.management.commands.import_csv import import_genre


class Command(BaseCommand):
    help = 'Загрузка данных из определённых csv файлов'

    def handle(self, *args, **options):
        import_genre()

        with open('static/data/users.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fields = CustomUser._meta.get_fields()
            print(reader.fieldnames)
            d = {}
            # здесь проверить интерсекцию в полях модели и названиях столбцов файла
            # или подставить дефолтное None для неописанных полей
            for field in fields[1:]:
                d[field.name] = None
            # print(d)
            for row in reader:
                # print(row)
                rd = {}
                for key, value in zip(d.keys(), row.values()):
                    # print(key, value, rd)
                    if isinstance(CustomUser._meta.get_field(key), models.ForeignKey):
                        # model = CustomUser.key.field.related_model.__name__
                        model = getattr(CustomUser, key).related_model.__name__
                        rd[key] = model.objects.get(id=value)
                    rd[key] = row.get(key, None)
                try:
                    CustomUser.objects.get(**rd)
                except CustomUser.DoesNotExist:
                    CustomUser.objects.create(**rd)