from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe
from .forms import RecipesSearchForm, RecipeAnalyticsForm

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        
        # Create a test recipe
        cls.test_recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="Test ingredient",
            cooking_time=30,
            difficulty="3"
        )

    def test_model_fields(self):
        """Test all model fields"""
        recipe = Recipe.objects.get(id=1)
        
        # Test field types and values
        self.assertEqual(recipe.name, "Test Recipe")
        self.assertEqual(recipe.ingredients, "Test ingredient")
        self.assertEqual(recipe.cooking_time, 30)
        self.assertEqual(recipe.difficulty, "3")
        
        # Test field max lengths
        self.assertEqual(recipe._meta.get_field('name').max_length, 120)
        
        # Test default image
        self.assertEqual(recipe.pic.name, 'no_image.jpg')

    def test_model_relationships(self):
        """Test model relationships"""
        recipe = Recipe.objects.get(id=1)
        recipe.saved_by.add(self.test_user)
        self.assertIn(self.test_user, recipe.saved_by.all())
        self.assertIn(recipe, self.test_user.saved_recipes.all())

    def test_string_representation(self):
        """Test string representation of model"""
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe), "Test Recipe")

    def test_absolute_url(self):
        """Test get_absolute_url method"""
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), f"/list/{recipe.pk}/")

class RecipeSearchFormTest(TestCase):
    def test_form_fields_presence(self):
        """Test all form fields are present"""
        form = RecipesSearchForm()
        self.assertIn('recipe_title', form.fields)
        self.assertIn('recipe_ingredients', form.fields)
        self.assertIn('difficulty_level', form.fields)
        self.assertIn('cooking_time', form.fields)

    def test_form_fields_validation(self):
        """Test form validation for all fields"""
        # Test valid data
        valid_data = {
            'recipe_title': 'Valid Recipe',
            'recipe_ingredients': 'ingredient1, ingredient2',
            'difficulty_level': '3',
            'cooking_time': 60
        }
        form = RecipesSearchForm(data=valid_data)
        self.assertTrue(form.is_valid())

        # Test invalid title (too short)
        invalid_data = valid_data.copy()
        invalid_data['recipe_title'] = 'ab'
        form = RecipesSearchForm(data=invalid_data)
        self.assertFalse(form.is_valid())

        # Test cooking time range
        invalid_data = valid_data.copy()
        invalid_data['cooking_time'] = -1
        form = RecipesSearchForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_form_cleaning(self):
        """Test form cleaning methods"""
        data = {
            'recipe_title': ' Test Recipe ',
            'recipe_ingredients': ' salt  ,  pepper , olive oil ',
            'difficulty_level': '3',
            'cooking_time': 60
        }
        form = RecipesSearchForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['recipe_ingredients'], 'salt,pepper,olive oil')
        self.assertEqual(form.cleaned_data['recipe_title'], 'Test Recipe')

class RecipeAnalyticsFormTest(TestCase):
    def test_analytics_form_fields(self):
        """Test analytics form fields"""
        form = RecipeAnalyticsForm()
        self.assertIn('analysis_type', form.fields)
        self.assertIn('chart_type', form.fields)

    def test_analytics_form_choices(self):
        """Test valid choices for analytics form"""
        form = RecipeAnalyticsForm()
        
        # Test analysis type choices
        valid_analysis_types = ['ingredients', 'difficulty', 'cooking_time']
        for choice in form.fields['analysis_type'].choices:
            self.assertIn(choice[0], valid_analysis_types)

        # Test chart type choices
        valid_chart_types = ['bar', 'pie', 'line']
        for choice in form.fields['chart_type'].choices:
            self.assertIn(choice[0], valid_chart_types)

class RecipeViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        
        # Create test recipes
        Recipe.objects.create(
            name="Test Recipe 1",
            ingredients="ingredient1, ingredient2",
            cooking_time=30,
            difficulty="3"
        )
        Recipe.objects.create(
            name="Test Recipe 2",
            ingredients="ingredient3, ingredient4",
            cooking_time=60,
            difficulty="4"
        )

    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        """Test recipe home view"""
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

    def test_list_view(self):
        """Test recipe list view"""
        # Test unauthenticated access
        response = self.client.get(reverse('recipes:list'))
        self.assertRedirects(response, '/login/?next=/list/')

        # Test authenticated access
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/main.html')
        self.assertTrue('form' in response.context)
        self.assertTrue('object_list' in response.context)

    def test_detail_view(self):
        """Test recipe detail view"""
        recipe = Recipe.objects.get(name="Test Recipe 1")
        
        # Test unauthenticated access
        response = self.client.get(
            reverse('recipes:recipe_detail', kwargs={'pk': recipe.pk})
        )
        self.assertRedirects(response, f'/login/?next=/list/{recipe.pk}/')

        # Test authenticated access
        self.client.login(username='testuser', password='12345')
        response = self.client.get(
            reverse('recipes:recipe_detail', kwargs={'pk': recipe.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/detail.html')
        self.assertEqual(response.context['object'], recipe)

    def test_analytics_view(self):
        """Test analytics view"""
        # Test unauthenticated access
        response = self.client.get(reverse('recipes:analytics'))
        self.assertRedirects(response, '/login/?next=/data/')

        # Test authenticated access
        self.client.login(username='testuser', password='12345')
        
        # Test GET request
        response = self.client.get(reverse('recipes:analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/analytics.html')
        self.assertTrue('form' in response.context)

        # Test POST request with valid data
        response = self.client.post(
            reverse('recipes:analytics'),
            {'analysis_type': 'difficulty', 'chart_type': 'bar'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('chart' in response.context)

    def test_my_recipes_view(self):
        """Test my recipes view"""
        # Login required
        self.client.login(username='testuser', password='12345')
        
        # Test with no saved recipes
        response = self.client.get(reverse('recipes:my_recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recipes']), 0)

        # Test with saved recipe
        recipe = Recipe.objects.get(name="Test Recipe 1")
        self.test_user.saved_recipes.add(recipe)
        response = self.client.get(reverse('recipes:my_recipes'))
        self.assertEqual(len(response.context['recipes']), 1)
        self.assertIn(recipe, response.context['recipes'])

    def test_save_recipe_view(self):
        """Test save recipe functionality"""
        self.client.login(username='testuser', password='12345')
        recipe = Recipe.objects.get(name="Test Recipe 1")
        
        # Test saving recipe
        response = self.client.post(
            reverse('recipes:save_recipe', kwargs={'recipe_id': recipe.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'saved')
        self.assertIn(recipe, self.test_user.saved_recipes.all())

        # Test unsaving recipe
        response = self.client.post(
            reverse('recipes:save_recipe', kwargs={'recipe_id': recipe.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'removed')
        self.assertNotIn(recipe, self.test_user.saved_recipes.all())

    def test_search_functionality(self):
        """Test recipe search functionality"""
        self.client.login(username='testuser', password='12345')
        
        # Test search by title
        response = self.client.post(
            reverse('recipes:list'),
            {
                'recipe_title': 'Test Recipe 1',
                'cooking_time': 360,
                'recipe_ingredients': '',
                'difficulty_level': ''
            }
        )
        self.assertEqual(len(response.context['recipe_list']), 1)

        # Test search by ingredients
        response = self.client.post(
            reverse('recipes:list'),
            {
                'recipe_title': '',
                'cooking_time': 360,
                'recipe_ingredients': 'ingredient1',
                'difficulty_level': ''
            }
        )
        self.assertEqual(len(response.context['recipe_list']), 1)

        # Test search by difficulty
        response = self.client.post(
            reverse('recipes:list'),
            {
                'recipe_title': '',
                'cooking_time': 360,
                'recipe_ingredients': '',
                'difficulty_level': '3'
            }
        )
        self.assertTrue(len(response.context['recipe_list']) >= 1)