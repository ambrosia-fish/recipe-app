# Generated by Django 4.2.17 on 2024-12-31 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("ingredients", models.TextField()),
                ("cooking_time", models.IntegerField()),
                ("difficulty", models.CharField(max_length=20)),
            ],
        ),
    ]
