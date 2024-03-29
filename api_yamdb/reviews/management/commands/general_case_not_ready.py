# import os
import csv

from django.core.management.base import BaseCommand
from django.db import models

from reviews.models import Category, CustomUser, Genre, Title  # Review,Comment


class Command(BaseCommand):
    help = 'Загрузка данных из определённых csv файлов'

#     def can_open_file(
#             self, path='static/data',
#             filenames=[
#                 'category.csv',
#                 'comments.csv',
#                 'genre.csv',
#                 'genre_title.csv',
#                 'review.csv',
#                 'titles.csv',
#                 'users.csv'
#             ]
#     ):
    #     """Проверяет возможность открытия файла.
    #     in: category.csv
    #     out: True/False"""
    #     path = 'static/data/'
    #     for file in filenames:
    #         file = path + file
    #         print(file)
    #         try:
    #             os.access(file, os.R_OK)
    #         except Exception as e:
    #             raise Exception(f'Проблемы с файлом {e}')
    # def get_file_names(self, path='static/data'):
    #     """Получает список файлов из директории, возвращает
    #     только название файла, без расширения.
    # in: [
    #     'category.csv',
    #     'comments.csv',
    #     'genre.csv',
    #     'genre_title.csv',
    #     'review.csv',
    #     'titles.csv',
    #     'users.csv']
    # out: [
    #      'category',
    #      'comments',
    #      'genre', 'genre_title', 'review', 'titles', 'users']"""
    #     files = os.listdir('static/data')
    #     print(files)
    #     self.can_open_file(files)
    #     names = list()
    #     while len(files) > 0:
    #         name = files.pop(0).split('.')[0]
    #         names.append(name)
    #     print(names)
    #     return names

    def import_genres(self):
        """Создаёт экземпляр класса csv, принимает в него файл csv. Создаёт
        словарь с парами ключ - поля модели, в которую произойдёт загрузка;
        значение - значене из файла, совпадающее с ключом. После словарь
        передаётся именованными аргументами в модель, пытаясь получить
        существующее значение в таблице либо создав новое."""
        # try:
        with open('static/data/genre.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fields = Genre._meta.get_fields()
            d = {}
            # здесь проверить интерсекцию в полях модели и названиях
            # столбцов файла или подставить дефолтное None
            # для неописанных полей
            for field in fields[1:]:
                d[field.name] = None
            for row in reader:
                rd = {}
                for key, value in zip(d.keys(), row.values()):
                    if isinstance(
                        Genre._meta.get_field(key), models.ForeignKey
                    ):
                        model = Genre.key.field.related_model.__name__
                        rd[key] = model.objects.get(id=value)
                    rd[key] = value
                try:
                    Genre.objects.get(**rd)
                except Genre.DoesNotExist:
                    Genre.objects.create(**rd)
        # except FileNotFoundError:
        #     print('Отсутствует файл genre.csv')

    def import_categories(self):
        try:
            with open(
                'static/data/category.csv', 'r', encoding='utf-8'
            ) as file:
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
        """Создаёт экземпляр класса csv, принимает в него файл csv. Создаёт
        словарь с парами ключ - поля модели, в которую произойдёт загрузка;
        значение - значене из файла, совпадающее с ключом. После словарь
        передаётся именованными аргументами в модель, пытаясь получить
        существующее значение в таблице либо создав новое."""
        # try:
        with open(
            'static/data/Titles.csv', 'r', encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            fields = Title._meta.get_fields()
            # print(reader.fieldnames)
            d = {}
            # здесь проверить интерсекцию в полях модели и названиях
            # столбцов файла или подставить дефолтное None
            # для неописанных полей
            for field in fields[1:]:
                d[field.name] = None
            # print(d)
            for row in reader:
                # print(row)
                rd = {}
                for key, value in zip(d.keys(), row.values()):
                    # print(key, value, rd)
                    if isinstance(
                        Title._meta.get_field(key), models.ForeignKey
                    ):
                        model = Title.key.related_model.__name__
                        # model = getattr(Title, key).related_model.__name__
                        rd[key] = model.objects.get(id=value)
                    rd[key] = row.get(key, None)
                try:
                    # print(rd)
                    Title.objects.get(**rd)
                except Title.DoesNotExist:
                    Title.objects.create(**rd)
        # except FileNotFoundError:
        #     print('Отсутствует файл genre.csv')

    def import_users(self):
        # try:
        with open('static/data/users.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fields = CustomUser._meta.get_fields()
            # print(reader.fieldnames)
            d = {}
            # здесь проверить интерсекцию в полях модели и названиях
            # столбцов файла или подставить дефолтное None
            # для неописанных полей
            for field in fields[1:]:
                d[field.name] = None
            # print(d)
            print(d)
            for row in reader:
                print(row)
                # if row.values() == None:

                # print(row)
                rd = {}
                # print(d.keys(), row.values())
                for key, value in zip(d.keys(), row.values()):
                    # print(key, value, rd)
                    print(rd)
                    if isinstance(
                        CustomUser._meta.get_field(key),
                        models.ManyToManyField
                    ):
                        # pass
                        model = CustomUser.key.related_model.__name__
                        # related_field_name =
                        # Model._meta.get_field(
                        # 'foreign_key_field').remote_field.name
                        # related_query_name =
                        # Model._meta.get_field(
                        # 'foreign_key_field').related_query_name()
                        # метод .set()????
                        # print(model)
                        # rd[key] = model.
                    if isinstance(
                        CustomUser._meta.get_field(key), models.ForeignKey
                    ):
                        model = CustomUser.key.related_model.__name__
                        # model =
                        # getattr(CustomUser, key).related_model.__name__
                        # print(model)
                        rd[key] = model.objects.get(id=value)
                    rd[key] = row.get(key, None)
                # if rd[key] is None:
                #     rd.pop(key)
                try:
                    print(rd)
                    CustomUser.objects.get(**rd)
                    pass
                except CustomUser.DoesNotExist:
                    CustomUser.objects.create(**rd)

    # def import_reviews(self):
        # try:
        #     with open(
        #         'static/data/review.csv', 'r', encoding='utf-8'
        #     ) as file:
        #         reader = csv.reader(file)
        #         next(reader)
        #         for row in reader:
        #             id = int(row[0])
        #             title_id = int(row[1])
        #             text = row[2]
        #             author = int(row[3])
        #             score = int(row[4])
        #             pub_date = row[5]
        #             try:
        #                 Review.objects.get(author=author, title=title_id)
        #             except Review.DoesNotExist:
        #                 Review.objects.create(
        #                     id=id,
        #                     title=Title.objects.get(id=title_id),
        #                     text=text,
        #                     author=CustomUser.objects.get(id=author),
        #                     score=score,
        #                     pub_date=pub_date
        #                 )
        # except FileNotFoundError:
        #     print('Отсутствует файл review.csv')

    # def import_comments(self):
    #     try:
    #         with open(
    #             'static/data/comments.csv', 'r', encoding='utf-8'
    #         ) as file:
    #             reader = csv.reader(file)
    #             next(reader)
    #             for row in reader:
    #                 id = int(row[0])
    #                 review_id = int(row[1])
    #                 text = row[2]
    #                 author = int(row[3])
    #                 pub_date = row[4]
    #                 try:
    #                     Comment.objects.get(id=id)
    #                 except Comment.DoesNotExist:
    #                     Comment.objects.create(
    #                         id=id,
    #                         review=Review.objects.get(id=review_id),
    #                         text=text,
    #                         author=CustomUser.objects.get(id=author),
    #                         pub_date=pub_date
    #                     )
    #     except FileNotFoundError:
    #         print('Отсутствует файл comments.csv')

    # def import_title_genres(self):
    #     try:
    #         with open(
    #             'static/data/genre_title.csv', 'r', encoding='utf-8'
    #         ) as file:
    #             reader = csv.reader(file)
    #             next(reader)
    #             for row in reader:
    #                 title_id = int(row[1])
    #                 genre_id = int(row[2])
    #                 try:
    #                     title = Title.objects.get(id=title_id)
    #                     genre = Genre.objects.get(id=genre_id)
    #                     if genre not in title.genre.all():
    #                         title.genre.add(genre)
    #                 except Title.DoesNotExist as e:
    #                     raise ValueError(
    #                         f'Произведение с id {title_id} не найдено: {e}'
    #                     )
    #                 except Genre.DoesNotExist as e:
    #                     raise ValueError(
    #                         f'Жанр с id {genre_id} не найден: {e}'
    #                     )
    #     except FileNotFoundError:
    #         print('Отсутствует файл genre_title.csv')

    def handle(self, *args, **options):
        try:
            # self.get_file_names()
            self.import_genres()
            self.import_categories()
            self.import_titles()
            # self.import_title_genres()
            self.import_users()
            # self.import_reviews()
            # self.import_comments()
        except Exception as e:
            raise Exception(f'Произошла ошибка при работе функции - {e}')
        finally:
            print('Работа функции окончена - с результатом или без оного.')
