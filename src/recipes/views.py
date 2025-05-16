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

# Set up logging
logger = logging.getLogger(__name__)

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/main.html"
    paginate_by = 12  # Reduced pagination for better performance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RecipesSearchForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        # First, attempt to limit everything for performance
        try:
            # Start with a very limited queryset
            queryset = Recipe.objects.all()[:20]  # Even more strict limit

            if self.request.method == "POST":
                form = RecipesSearchForm(self.request.POST)
                if form.is_valid():
                    # Apply filters with stricter limits
                    recipe_title = form.cleaned_data.get("recipe_title")
                    recipe_ingredients = form.cleaned_data.get("recipe_ingredients")
                    difficulty_level = form.cleaned_data.get("difficulty_level")
                    cooking_time = form.cleaned_data.get("cooking_time", 120)  # Default to 2 hours max

                    # Apply each filter carefully and with timeouts
                    if difficulty_level:
                        queryset = queryset.filter(difficulty__lte=difficulty_level)
                        
                    # Stricter cooking time limit
                    queryset = queryset.filter(cooking_time__lte=min(cooking_time, 120))
                        
                    if recipe_title:
                        queryset = queryset.filter(name__icontains=recipe_title)
                        
                    if recipe_ingredients:
                        # Only use the first ingredient for better performance
                        ingredients_list = [
                            ing.strip() 
                            for ing in recipe_ingredients.split(",") 
                            if ing.strip()
                        ][:1]  # Limit to first ingredient only
                        
                        if ingredients_list:
                            queryset = queryset.filter(ingredients__icontains=ingredients_list[0])
            
            # Final safety limit
            return queryset[:20]  # Very strict limit
            
        except Exception as e:
            # Log any database errors
            logger.error(f"Database error in get_queryset: {str(e)}")
            # Return empty queryset as fallback
            return Recipe.objects.none()


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_object(self, queryset=None):
        try:
            # Add a small timeout for database queries
            return super().get_object(queryset)
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
                recipes = Recipe.objects.all()[:20]

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
