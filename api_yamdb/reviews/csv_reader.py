import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
import csv
from reviews.models import *

with open('genre.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        id = row[0]
        name = row[1]
        slug = row[2]
        try:
            Genre.objects.get(slug=slug)
        except:
            Genre.objects.create(id=id, name=name, slug=slug)

with open('category.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        id = row[0]
        name = row[1]
        slug = row[2]
        try:
            Category.objects.get(slug=slug)
        except:
            Category.objects.create(id=id, name=name, slug=slug)

with open('titles.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        id = int(row[0])
        name = row[1]
        year = int(row[2])
        category = int(row[3])
    try:
        Title.objects.get(id=id, name=name, year=year, category=category)
    except:
        Title.objects.create(id=id, name=name, year=year, category=category)

with open('users.csv', 'r') as file:
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
    except:
        CustomUser.objects.create(
            id=id,
            username=username,
            email=email,
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name
        )

with open('review.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        id = int(row[0])
        title_id = int(row[1])
        text = row[2]
        author = row[3]
        score = int(row[4])
        pub_date = row[5]
    try:
        Review.objects.get(author=author, title=title_id)
    except:
        Review.objects.create(
            id=id,
            title=title_id,
            text=text,
            author=author,
            score=score,
            pub_date=pub_date
        )

with open('comments.csv', 'r') as file:
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
    except:
        Comment.objects.create(
            id=id,
            review=review_id,
            text=text,
            author=author,
            pub_date=pub_date
        )
