# src/recipes/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RecipesSearchForm, RecipeAnalyticsForm
from .utils import create_chart


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RecipesSearchForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Recipe.objects.all()

        if self.request.method == "POST":
            form = RecipesSearchForm(self.request.POST)
            if form.is_valid():
                recipe_title = form.cleaned_data.get("recipe_title")
                recipe_ingredients = form.cleaned_data.get("recipe_ingredients")
                difficulty_level = form.cleaned_data.get("difficulty_level")
                cooking_time = form.cleaned_data[
                    "cooking_time"
                ]  # Will always have a value

                if difficulty_level:
                    queryset = queryset.filter(difficulty__lte=difficulty_level)

                queryset = queryset.filter(cooking_time__lte=cooking_time)

                if recipe_title:
                    queryset = queryset.filter(name__icontains=recipe_title)

                if recipe_ingredients:
                    ingredients_list = [
                        ing.strip()
                        for ing in recipe_ingredients.split(",")
                        if ing.strip()
                    ]
                    ingredients_query = Q()
                    for ingredient in ingredients_list:
                        ingredients_query |= Q(ingredients__icontains=ingredient)
                    queryset = queryset.filter(ingredients_query)

        return queryset


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/detail.html"


class RecipeAnalyticsView(LoginRequiredMixin, TemplateView):
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

            # Get all recipes
            recipes = Recipe.objects.all()

            if recipes:
                chart = create_chart(chart_type, recipes, analysis_type)
                context["chart"] = chart

        return self.render_to_response(context)


@login_required
def recipe_home(request):
    return render(request, "recipes/recipes_home.html")
