from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RecipesSearchForm, RecipeAnalyticsForm
from .utils import create_chart
from django.http import JsonResponse
import logging
import time
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Set up logging
logger = logging.getLogger(__name__)

# Apply cache to the recipe list view (2 minute cache)
@method_decorator(cache_page(120), name='dispatch')
class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/main.html"
    paginate_by = None  # Disable pagination to avoid extra queries

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RecipesSearchForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        # Use cache if possible to avoid database hits
        cache_key = 'recipe_list'
        
        if self.request.method == "POST":
            cache_key = 'recipe_search_' + str(hash(frozenset(self.request.POST.items())))
        
        queryset = cache.get(cache_key)
        
        if queryset is not None:
            logger.debug(f"Using cached queryset for {cache_key}")
            return queryset
            
        # If not in cache, get from database with strict limits
        try:
            # Start with a very limited queryset
            queryset = list(Recipe.objects.all()[:20])  # Convert to list to avoid future queries

            if self.request.method == "POST":
                form = RecipesSearchForm(self.request.POST)
                if form.is_valid():
                    # Apply filters with stricter limits
                    recipe_title = form.cleaned_data.get("recipe_title")
                    recipe_ingredients = form.cleaned_data.get("recipe_ingredients")
                    difficulty_level = form.cleaned_data.get("difficulty_level")
                    cooking_time = form.cleaned_data.get("cooking_time", 120)  # Default to 2 hours max

                    # Apply filters to the in-memory list to avoid database queries
                    filtered_queryset = []
                    for recipe in queryset:
                        # Apply difficulty filter
                        if difficulty_level and recipe.difficulty > difficulty_level:
                            continue
                            
                        # Apply cooking time filter
                        if recipe.cooking_time > min(cooking_time, 120):
                            continue
                            
                        # Apply title filter
                        if recipe_title and recipe_title.lower() not in recipe.name.lower():
                            continue
                            
                        # Apply ingredients filter
                        if recipe_ingredients:
                            ingredients_list = [ing.strip() for ing in recipe_ingredients.split(",") if ing.strip()][:1]
                            if ingredients_list and not any(ing.lower() in recipe.ingredients.lower() for ing in ingredients_list):
                                continue
                                
                        filtered_queryset.append(recipe)
                    
                    queryset = filtered_queryset[:20]  # Apply final limit
            
            # Cache the result for 2 minutes
            cache.set(cache_key, queryset, 120)
            return queryset
            
        except Exception as e:
            # Log any database errors
            logger.error(f"Database error in get_queryset: {str(e)}")
            # Return empty queryset as fallback
            return []


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_object(self, queryset=None):
        try:
            # Check cache first
            cache_key = f'recipe_detail_{self.kwargs["pk"]}'
            cached_object = cache.get(cache_key)
            
            if cached_object:
                return cached_object
                
            # If not in cache, get from database
            obj = super().get_object(queryset)
            
            # Cache for 2 minutes
            cache.set(cache_key, obj, 120)
            return obj
            
        except Exception as e:
            logger.error(f"Error retrieving recipe: {str(e)}")
            # Return None, template will handle this gracefully
            return None


class RecipeAnalyticsView(TemplateView):
    template_name = "recipes/analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RecipeAnalyticsForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        form = RecipeAnalyticsForm(request.POST)
        context = self.get_context_data()

        if form.is_valid():
            chart_type = form.cleaned_data.get("chart_type")
            analysis_type = form.cleaned_data.get("analysis_type")

            try:
                # Get recipes with stricter limit
                recipes = Recipe.objects.all()[:15]

                if recipes:
                    chart = create_chart(chart_type, recipes, analysis_type)
                    context["chart"] = chart
            except Exception as e:
                logger.error(f"Error in analytics: {str(e)}")
                context["error"] = "Could not generate chart due to database issues."

        return self.render_to_response(context)


def recipe_home(request):
    return render(request, "recipes/recipes_home.html")


def save_recipe(request, recipe_id):
    # Check if user is authenticated before saving
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "error", 
            "message": "Authentication is currently disabled. Recipe saving is unavailable."
        })
    
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        if recipe in request.user.saved_recipes.all():
            request.user.saved_recipes.remove(recipe)
            return JsonResponse({"status": "removed"})
        else:
            request.user.saved_recipes.add(recipe)
            return JsonResponse({"status": "saved"})
    except Recipe.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Recipe not found"})
    except Exception as e:
        logger.error(f"Error saving recipe: {str(e)}")
        return JsonResponse({"status": "error", "message": "Database connection error"})


def my_recipes(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Return empty list for non-authenticated users
        return render(request, "recipes/my_recipes.html", {"recipes": []})
    
    try:
        saved_recipes = request.user.saved_recipes.all()[:10]  # Strict limit
        return render(request, "recipes/my_recipes.html", {"recipes": saved_recipes})
    except Exception as e:
        logger.error(f"Error retrieving saved recipes: {str(e)}")
        return render(request, "recipes/my_recipes.html", {"recipes": [], "error": "Database connection error"})
