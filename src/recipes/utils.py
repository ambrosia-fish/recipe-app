# in recipes/utils.py
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import pandas as pd


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph


def get_ingredients_data(recipes):
    all_ingredients = []
    for recipe in recipes:
        ingredients = [i.strip() for i in recipe.ingredients.split(",")]
        all_ingredients.extend(ingredients)

    ingredient_counts = pd.Series(all_ingredients).value_counts().head(10)
    return ingredient_counts


def create_chart(chart_type, data, analysis_type):
    plt.switch_backend("AGG")
    plt.figure(figsize=(10, 6))
    plt.title(f"{analysis_type.title()} Analysis")

    if analysis_type == "ingredients":
        data = get_ingredients_data(data)
        if chart_type == "bar":
            plt.bar(data.index, data.values)
            plt.xticks(rotation=45, ha="right")
        elif chart_type == "pie":
            plt.pie(data.values, labels=data.index, autopct="%1.1f%%")
        elif chart_type == "line":
            plt.plot(data.index, data.values, marker="o")
            plt.xticks(rotation=45, ha="right")

    elif analysis_type == "difficulty":
        difficulty_counts = (
            pd.Series([r.difficulty for r in data]).value_counts().sort_index()
        )
        if chart_type == "bar":
            plt.bar(difficulty_counts.index, difficulty_counts.values)
            plt.xlabel("Difficulty Level")
            plt.ylabel("Number of Recipes")
        elif chart_type == "pie":
            plt.pie(
                difficulty_counts.values,
                labels=[f"Level {i}" for i in difficulty_counts.index],
                autopct="%1.1f%%",
            )
        elif chart_type == "line":
            plt.plot(difficulty_counts.index, difficulty_counts.values, marker="o")
            plt.xlabel("Difficulty Level")
            plt.ylabel("Number of Recipes")

    elif analysis_type == "cooking_time":
        cooking_times = [r.cooking_time for r in data]
        if chart_type == "bar":
            plt.hist(cooking_times, bins=10, edgecolor="black")
            plt.xlabel("Cooking Time (minutes)")
            plt.ylabel("Number of Recipes")
        elif chart_type == "pie":
            # Create time ranges for pie chart
            ranges = pd.cut(
                cooking_times,
                bins=5,
                labels=["0-60", "61-120", "121-180", "181-240", "241+"],
            )
            range_counts = ranges.value_counts()
            plt.pie(range_counts.values, labels=range_counts.index, autopct="%1.1f%%")
        elif chart_type == "line":
            times_series = pd.Series(cooking_times).sort_values()
            plt.plot(range(len(times_series)), times_series, marker="o")
            plt.xlabel("Recipe Index")
            plt.ylabel("Cooking Time (minutes)")

    plt.tight_layout()
    chart = get_graph()
    return chart
