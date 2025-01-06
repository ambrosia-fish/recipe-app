# src/recipes/urls.py
from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_home, name='home'),  
]