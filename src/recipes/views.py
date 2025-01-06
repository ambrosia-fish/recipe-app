from django.shortcuts import render

def recipe_home(request):
    return render(request,'recipes/recipes_home.html')
