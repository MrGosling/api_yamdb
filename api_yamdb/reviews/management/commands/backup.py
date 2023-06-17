from django.core.management.base import BaseCommand
from django.db import models
import csv
from reviews.models import Genre, Category, Title, CustomUser, Review, Comment


class Command(BaseCommand):
    help = 'Загрузка данных из определённых csv файлов'

    def import_genres(self):
        try:
            with open('static/data/genre.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fields = Genre._meta.get_fields()
                d = {}
                # здесь проверить интерсекион в полях модели и названиях столбцов файла
                # или подставить дефолтное ноне для неописанных полей
                for field in fields[1:]:
                    d[field.name] = None
                for row in reader:
                    rd = {}
                    for key, value in zip(d.keys(), row.values()):
                        if isinstance(Genre._meta.get_field(key), models.ForeignKey):
                            model = Genre.key.field.related_model.__name__
                            rd[key] = model.objects.get(id=value)
                        rd[key] = value
                    try:
                        Genre.objects.get(**rd)
                    except Genre.DoesNotExist:
                        Genre.objects.create(**rd)
        except FileNotFoundError:
            print('Отсутствует файл genre.csv')
    
    def import_categories(self):
        try:
            with open('static/data/category.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fields = Category._meta.get_fields()
                d = {}
                for field in fields[1:]:
                    d[field.name] = None
                for row in reader:
                    rd = {}
                    for key, value in zip(d.keys(), row.values()):
                        rd[key] = value
                    try:
                        Category.objects.filter(**rd).exists()
                    except Category.DoesNotExist:
                        Category.objects.create(**rd)
        except FileNotFoundError:
            print('Отсутствует файл category.csv')
    
    def import_titles(self):
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

    def import_users(self):
        try:
            with open('static/data/users.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    id = row[0]
                    username = row[1]
                    email = row[2]
                    role = row[3]
                    bio = row[4]
                    first_name = row[5]
                    last_name = row[6]
                    try:
                        CustomUser.objects.get(username=username)
                    except CustomUser.DoesNotExist:
                        CustomUser.objects.create(
                            id=id,
                            username=username,
                            email=email,
                            role=role,
                            bio=bio,
                            first_name=first_name,
                            last_name=last_name
                        )
        except FileNotFoundError:
            print('Отсутствует файл users.csv')

    def import_reviews(self):
        try:
            with open('static/data/review.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    id = int(row[0])
                    title_id = int(row[1])
                    text = row[2]
                    author = int(row[3])
                    score = int(row[4])
                    pub_date = row[5]
                    try:
                        Review.objects.get(author=author, title=title_id)
                    except Review.DoesNotExist:
                        Review.objects.create(
                            id=id,
                            title=Title.objects.get(id=title_id),
                            text=text,
                            author=CustomUser.objects.get(id=author),
                            score=score,
                            pub_date=pub_date
                        )
        except FileNotFoundError:
            print('Отсутствует файл review.csv')

    def import_comments(self):
        try:
            with open('static/data/comments.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    id = int(row[0])
                    review_id = int(row[1])
                    text = row[2]
                    author = int(row[3])
                    pub_date = row[4]
                    try:
                        Comment.objects.get(id=id)
                    except Comment.DoesNotExist:
                        Comment.objects.create(
                            id=id,
                            review=Review.objects.get(id=review_id),
                            text=text,
                            author=CustomUser.objects.get(id=author),
                            pub_date=pub_date
                        )
        except FileNotFoundError:
            print('Отсутствует файл comments.csv')

    def import_title_genres(self):
        try:
            with open('static/data/genre_title.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    title_id = int(row[1])
                    genre_id = int(row[2])
                    try:
                        title = Title.objects.get(id=title_id)
                        genre = Genre.objects.get(id=genre_id)
                        if genre not in title.genre.all():
                            title.genre.add(genre)
                    except Title.DoesNotExist as e:
                        raise ValueError(f'Произведение с id {title_id} не найдено: {e}')
                    except Genre.DoesNotExist as e:
                        raise ValueError(f'Жанр с id {genre_id} не найден: {e}')
        except FileNotFoundError:
            print('Отсутствует файл genre_title.csv')

    def handle(self, *args, **options):
        try:
            self.import_genres()
            self.import_categories()
            self.import_titles()
            self.import_title_genres()
            self.import_users()
            self.import_reviews()
            self.import_comments()
        except Exception as e:
            raise Exception(f'Произошла ошибка при работе функции - {e}')
        finally:
            print('Работа функции окончена - с результатом или без оного.')
