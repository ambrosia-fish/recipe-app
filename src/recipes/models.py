# src/recipes/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Recipe(models.Model):
    saved_by = models.ManyToManyField(User, related_name='saved_recipes', blank=True)
    name = models.CharField(max_length=120)
    ingredients = models.TextField()
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=20)
    pic = models.ImageField(upload_to="recipes", default="no_image.jpg")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipes:recipe_detail", kwargs={"pk": self.pk})
