from .models import Rating
from statistics import mean


def list_recipes(recipe_query):
    all_recipes = []

    for recipe in recipe_query:

        ingredients = list(recipe.ingredients.values_list('name', flat=True))

        rates_list = list(Rating.objects.filter(recipe=recipe).values_list("rate_id", flat=True))

        if rates_list:
            average_rating = round(mean(rates_list), 2)
        else:
            average_rating = "This recipe is not rated yet."
        recipe_data = {
            "recipe_name": recipe.name,
            "recipe_text": recipe.recipe_text,
            "ingredients": ingredients,
            "average_rating": average_rating,
            "created_by": recipe.user.email
        }
        all_recipes.append(recipe_data)
    content = {
        "status": 200,
        "found_recipes": len(all_recipes),
        "recipes": all_recipes
    }
    return content
