from django.urls import path
from .views import RecipeListView, RecipeDetailView, recipe_home, RecipeAnalyticsView

app_name = "recipes"

urlpatterns = [
    path("", recipe_home, name="home"),
    path("list/", RecipeListView.as_view(), name="list"),
    path("list/<pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("data/", RecipeAnalyticsView.as_view(), name="analytics"),
]
