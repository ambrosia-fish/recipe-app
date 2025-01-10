# src/recipes/models.py
from django.db import models
from django.urls import reverse


class Recipe(models.Model):
    name = models.CharField(max_length=120)
    ingredients = models.TextField()
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=20)
    pic = models.ImageField(upload_to="recipes", default="no_image.jpg")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipes:recipe_detail", kwargs={"pk": self.pk})
