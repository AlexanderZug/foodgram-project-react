import json
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Upload data to Ingredients model"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Start command"))
        with open(os.path.abspath("data/ingredients.json")) as data_file:
            json_data = json.loads(data_file.read())
            for ingredients in json_data:
                Ingredient.objects.get_or_create(**ingredients)
            self.stdout.write(self.style.SUCCESS("Data is uploaded"))
