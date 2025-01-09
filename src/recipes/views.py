#src/recipes/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RecipesSearchForm

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RecipesSearchForm(self.request.POST or None)
        return context
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Recipe.objects.all()
        
        if self.request.method == 'POST':
            form = RecipesSearchForm(self.request.POST)
            if form.is_valid():
                recipe_title = form.cleaned_data.get('recipe_title')
                recipe_ingredients = form.cleaned_data.get('recipe_ingredients')
                difficulty_level = form.cleaned_data.get('difficulty_level')
                cooking_time = form.cleaned_data['cooking_time']  # Will always have a value


                # Apply difficulty filter
                if difficulty_level:
                    queryset = queryset.filter(difficulty__lte=difficulty_level)
                
                # Always apply cooking time filter (slider always has a value)
                queryset = queryset.filter(cooking_time__lte=cooking_time)
                
                # Apply title filter if provided
                if recipe_title:
                    queryset = queryset.filter(name__icontains=recipe_title)
                
                # Apply ingredients filter if provided
                if recipe_ingredients:
                    ingredients_list = [ing.strip() for ing in recipe_ingredients.split(',') if ing.strip()]
                    ingredients_query = Q()
                    for ingredient in ingredients_list:
                        ingredients_query |= Q(ingredients__icontains=ingredient)
                    queryset = queryset.filter(ingredients_query)

        return queryset

class RecipeDetailView(LoginRequiredMixin, DetailView):                       
   model = Recipe                                        
   template_name = 'recipes/detail.html'                 

@login_required
def recipe_home(request):
    return render(request, 'recipes/recipes_home.html')