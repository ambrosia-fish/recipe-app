from django.test import TestCase
from .models import Recipe

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(
            name='Test Recipe',
            ingredients='Test ingredient',
            cooking_time=30,
            difficulty='Easy'
        )

    def test_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)

    def test_recipe_str(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe), 'Test Recipe')