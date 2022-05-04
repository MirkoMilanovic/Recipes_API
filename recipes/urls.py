from django.urls import path
from .views import CreateRecipeView, AllRecipesView, MyRecipesView,  RateRecipeView, MostUsedIngredientsView, SearchRecipesView, FilterRecipesView


urlpatterns = [
    path('create_recipe', CreateRecipeView.as_view(), name="create_recipe"),
    path('all_recipes', AllRecipesView.as_view(), name="all_recipes"),
    path('my_recipes', MyRecipesView.as_view(), name="my_recipes"),
    path('rate_recipe', RateRecipeView.as_view(), name="rate_recipe"),
    path('most_used_ingredients', MostUsedIngredientsView.as_view(), name="most_used_ingredients"),
    path('search_recipes', SearchRecipesView.as_view(), name="search_recipes"),
    path('filter_recipes', FilterRecipesView.as_view(), name="filter_recipes")
]
