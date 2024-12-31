from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=120)
    ingredients = models.TextField()
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.name