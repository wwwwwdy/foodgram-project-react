from django.core.management.base import BaseCommand
from recipe.models import Ingredient
import csv
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        for csv_file in options['csv_file']:
            dataReader = csv.reader(open(csv_file, encoding='utf-8'), delimiter=',', quotechar='"')
            for row in dataReader:
#                 row = [entry.decode("cp1251", "replace") for entry in row]
#                 row = [entry.decode("utf8", "replace") for entry in row]
                ingredient = Ingredient(name=row[0], measurement_unit=row[1])
                ingredient.save()

# import csv
#
# from django.core.management.base import BaseCommand
#
#
# class Command(BaseCommand):
#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', nargs='+', type=str)
#
#     def handle(self, *args, **options):
#         with open('../../data/ingredients.csv', newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 ingredient = Ingredient.objects.create(*row)
#                 ingredient.save()

#         with open('static/data/category.csv', newline='',
#                   encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             obj_list = []
#             for row in reader:
#                 obj = Category(**row)
#                 obj_list.append(obj)
#             Category.objects.bulk_create(obj_list)