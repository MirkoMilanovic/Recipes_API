from django.test import TestCase
from recipes.models import Ingredient, Recipe, Rating, Rate
from users.models import User


class TestModels(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email = 'petar@m.com',
            first_name = "Petar",
            last_name = "Petrovic",
            password = 'petar123',
        )
        self.ingredient1 = Ingredient.objects.create(
            name = "Salt"
        )
        self.ingredient2 = Ingredient.objects.create(
            name = "Sugar"
        )
        self.recipe1 = Recipe.objects.create(
            name = "Recipe1",
            recipe_text = "Recipe text",
            user = self.user1
        )
        self.recipe1.ingredients.add(self.ingredient1)
        self.recipe1.ingredients.add(self.ingredient2)

        self.rate1 = Rate.objects.create(
            rate = 5
        )
        self.rating1 = Rating.objects.create(
            user = self.user1,
            recipe = self.recipe1,
            rate = self.rate1
        )


    def test_ingredient(self):
        self.assertEquals(self.ingredient1.name, "Salt")


    def test_recipe(self):
        self.assertEquals(self.recipe1.name, "Recipe1")
        self.assertEquals(self.recipe1.user.first_name, "Petar")


    def test_recipe_ingredients(self):
        self.assertEquals(self.recipe1.ingredients.count(), 2)


    def test_rate(self):
        self.assertEquals(self.rate1.rate, 5)


    def test_rating(self):
        self.assertEquals(self.rating1.user.first_name, "Petar")
        self.assertEquals(self.rating1.recipe.name, "Recipe1")
        self.assertEquals(self.rating1.rate.rate, 5)