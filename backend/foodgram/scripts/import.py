import csv

from ingredients.models import Ingredients
from tags.models import Tags


def ingredients_import():
    with open('static/data/ingredients.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            ingredient = Ingredients.objects.create(
                name=row[0],
                measurement_unit=row[1]
            )
            ingredient.save()


def tags_import():
    with open('static/data/tags.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        Tags.objects.all().delete()
        for row in reader:
            print(row)
            tag = Tags.objects.create(name=row[0],
                                      color=row[1],
                                      slug=row[2])
            tag.save()


def run():
    ingredients_import()
    tags_import()
