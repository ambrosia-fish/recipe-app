from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipesSearchForm, RecipeAnalyticsForm

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

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), '/list/1/')

class RecipeSearchFormTest(TestCase):
    def test_recipe_title_field_label(self):
        form = RecipesSearchForm()
        self.assertTrue(form.fields['recipe_title'].label is None or 
                       form.fields['recipe_title'].label == 'Recipe title')

    def test_recipe_title_validation(self):
        form_data = {
            'recipe_title': 'ab',
            'cooking_time': 360,
            'recipe_ingredients': '',
            'difficulty_level': ''
        }
        form = RecipesSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        form_data = {
            'recipe_title': 'valid recipe',
            'cooking_time': 360,
            'recipe_ingredients': '',
            'difficulty_level': ''
        }
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_ingredients_cleaning(self):
        form_data = {
            'recipe_title': '',
            'recipe_ingredients': ' salt  ,  pepper,olive oil  ',
            'difficulty_level': '',
            'cooking_time': 360
        }
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['recipe_ingredients'], 'salt,pepper,olive oil')

    def test_cooking_time_range(self):
        form = RecipesSearchForm()
        self.assertEqual(form.fields['cooking_time'].min_value, 0)
        self.assertEqual(form.fields['cooking_time'].max_value, 360)

class RecipeAnalyticsFormTest(TestCase):
    def test_required_fields(self):
        form = RecipeAnalyticsForm()
        self.assertTrue(form.fields['analysis_type'].required)
        self.assertTrue(form.fields['chart_type'].required)

    def test_valid_choices(self):
        form_data = {
            'analysis_type': 'ingredients',
            'chart_type': 'bar'
        }
        form = RecipeAnalyticsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_choices(self):
        form_data = {
            'analysis_type': 'invalid',
            'chart_type': 'invalid'
        }
        form = RecipeAnalyticsForm(data=form_data)
        self.assertFalse(form.is_valid())

class RecipeViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='testuser', password='12345')
        Recipe.objects.create(
            name='Test Recipe 1',
            ingredients='ingredient1, ingredient2',
            cooking_time=30,
            difficulty='3'
        )
        Recipe.objects.create(
            name='Test Recipe 2',
            ingredients='ingredient3, ingredient4',
            cooking_time=60,
            difficulty='4'
        )

    def setUp(self):
        self.client = Client()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('recipes:list'))
        self.assertRedirects(response, '/login/?next=/list/')

    def test_logged_in_user_can_access_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/main.html')

    def test_recipe_search_filtering(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('recipes:list'), {
            'recipe_title': 'Test Recipe 1',
            'cooking_time': 360,
            'recipe_ingredients': '',
            'difficulty_level': ''
        })
        self.assertEqual(len(response.context['recipe_list']), 1)

    def test_analytics_view_protection(self):
        response = self.client.get(reverse('recipes:analytics'))
        self.assertRedirects(response, '/login/?next=/data/')
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/analytics.html')

    def test_analytics_chart_generation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('recipes:analytics'), {
            'analysis_type': 'difficulty',
            'chart_type': 'bar'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('chart' in response.context)

    def test_detail_view_protection(self):
        recipe = Recipe.objects.get(name='Test Recipe 1')
        response = self.client.get(
            reverse('recipes:recipe_detail', kwargs={'pk': recipe.pk})
        )
        self.assertRedirects(
            response, 
            f'/login/?next=/list/{recipe.pk}/'
        )
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get(
            reverse('recipes:recipe_detail', kwargs={'pk': recipe.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/detail.html')