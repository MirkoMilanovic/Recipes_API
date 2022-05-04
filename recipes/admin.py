from django.contrib import admin
from .models import Ingredient, Recipe, Rating, Rate


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    model = Recipe


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    model = Rate


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    model = Rating