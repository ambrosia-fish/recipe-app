from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RecipesSearchForm, RecipeAnalyticsForm
from .utils import create_chart
from django.http import JsonResponse
import logging

# Set up logging
logger = logging.getLogger(__name__)

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/main.html"
    paginate_by = 20  # Added pagination

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RecipesSearchForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        # Start with a limited queryset to avoid huge result sets
        queryset = Recipe.objects.all()[:200]  

        if self.request.method == "POST":
            form = RecipesSearchForm(self.request.POST)
            if form.is_valid():
                # Apply filters with limits
                recipe_title = form.cleaned_data.get("recipe_title")
                recipe_ingredients = form.cleaned_data.get("recipe_ingredients")
                difficulty_level = form.cleaned_data.get("difficulty_level")
                cooking_time = form.cleaned_data.get("cooking_time", 300)  # Default to 5 hours max

                # Apply each filter separately and carefully
                if difficulty_level:
                    queryset = queryset.filter(difficulty__lte=difficulty_level)
                    
                # Limit cooking time results
                queryset = queryset.filter(cooking_time__lte=min(cooking_time, 300))  # Cap at 5 hours
                    
                if recipe_title:
                    queryset = queryset.filter(name__icontains=recipe_title)
                    
                if recipe_ingredients:
                    # Simplify ingredient filtering and limit to first 3 ingredients
                    ingredients_list = [
                        ing.strip() 
                        for ing in recipe_ingredients.split(",") 
                        if ing.strip()
                    ][:3]  # Limit to first 3 ingredients for performance
                    
                    # Use a simpler approach to filtering - one by one
                    for ingredient in ingredients_list:
                        queryset = queryset.filter(ingredients__icontains=ingredient)
        
        # Final safety limit
        return queryset[:100]  # Always limit results


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"


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

            # Get recipes with a limit for performance
            recipes = Recipe.objects.all()[:100]

            if recipes:
                chart = create_chart(chart_type, recipes, analysis_type)
                context["chart"] = chart

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
        return JsonResponse({"status": "error", "message": "An error occurred"})


def my_recipes(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Return empty list for non-authenticated users
        return render(request, "recipes/my_recipes.html", {"recipes": []})
    
    saved_recipes = request.user.saved_recipes.all()[:50]  # Limit for performance
    return render(request, "recipes/my_recipes.html", {"recipes": saved_recipes})
