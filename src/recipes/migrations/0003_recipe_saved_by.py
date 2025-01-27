# Generated by Django 4.2.17 on 2025-01-13 19:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0002_recipe_pic"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="saved_by",
            field=models.ManyToManyField(
                blank=True, related_name="saved_recipes", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
