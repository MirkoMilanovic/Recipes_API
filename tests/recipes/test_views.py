from rest_framework.exceptions import ParseError
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from recipes.models import Ingredient, Recipe, Rate
from recipes import views
import mock


@mock.patch.object(views, "user_detection", return_value=1)
class TestViews(APITestCase):
    def setUp(self):

        self.client = APIClient()

        self.create_recipe_url = reverse('create_recipe')
        self.all_recipes_url = reverse('all_recipes')
        self.my_recipes_url = reverse('my_recipes')
        self.rate_recipe_url = reverse('rate_recipe')
        self.most_used_ingredients_url = reverse('most_used_ingredients')
        self.search_recipes_url = reverse('search_recipes')
        self.filter_recipes_url = reverse('filter_recipes')

        self.user1 = User.objects.create(
            email = "user1@stripe.com",
            first_name = "Name1",
            last_name = "Lastname1",
            password = "123"
        )
        self.user1.set_password('123')
        self.user1.save()

        self.user2 = User.objects.create(
            email = "user2@stripe.com",
            first_name = "Name2",
            last_name = "Lastname2",
            password = "456"
        )
        self.user2.set_password('456')
        self.user2.save()

        self.ingredient1 = Ingredient.objects.create(name = "Ing1")
        self.ingredient2 = Ingredient.objects.create(name = "Ing2")
        self.ingredient3 = Ingredient.objects.create(name = "Ing3")
        self.ingredient4 = Ingredient.objects.create(name = "Ing4")     
        self.ingredient5 = Ingredient.objects.create(name = "Ing5")
        self.ingredient6 = Ingredient.objects.create(name = "Ing6")
        self.ingredient7 = Ingredient.objects.create(name = "Ing7")
        self.ingredient8 = Ingredient.objects.create(name = "Ing8")
        self.ingredient9 = Ingredient.objects.create(name = "Ing9")

        self.recipe1 = Recipe.objects.create(
            name = "Recipe1",
            recipe_text = "Recipe1 text.",
            user = self.user1
        )
        self.recipe1.ingredients.add(self.ingredient1)
        self.recipe1.ingredients.add(self.ingredient2)
        self.recipe1.ingredients.add(self.ingredient3)
        self.recipe1.ingredients.add(self.ingredient4)
        self.recipe1.ingredients.add(self.ingredient5)

        self.recipe2 = Recipe.objects.create(
            name = "Recipe2",
            recipe_text = "Recipe2 text.",
            user = self.user1
        )
        self.recipe2.ingredients.add(self.ingredient1)
        self.recipe2.ingredients.add(self.ingredient2)
        self.recipe2.ingredients.add(self.ingredient3)
        self.recipe2.ingredients.add(self.ingredient4)
        self.recipe2.ingredients.add(self.ingredient5)

        self.recipe3 = Recipe.objects.create(
            name = "Recipe3",
            recipe_text = "Recipe3 text.",
            user = self.user1
        )
        self.recipe3.ingredients.add(self.ingredient1)
        self.recipe3.ingredients.add(self.ingredient2)
        self.recipe3.ingredients.add(self.ingredient3)
        self.recipe3.ingredients.add(self.ingredient6)

        self.recipe4 = Recipe.objects.create(
            name = "Recipe4",
            recipe_text = "Recipe4 text.",
            user = self.user2
        )
        self.recipe4.ingredients.add(self.ingredient7)
        self.recipe4.ingredients.add(self.ingredient8)
        self.recipe4.ingredients.add(self.ingredient9)

        self.data_create_recipe = {
            "recipe_name": "Recipe5",
            "recipe_text": "Recipe5 text.",
            "ingredients_list": ["Ing1", "Ing2", "Ing10"]
        }
        self.data_create_recipe_incomplete = {
            "recipe_name": "Recipe5",
            "ingredients_list": ["Ing1", "Ing2", "Ing10"]
        }
        self.data_create_recipe_wrong = {
            "recipe_name": 5,
            "recipe_text": "Recipe5 text.",
            "ingredients_list": ["Ing1", 2, "Ing10"]
        }
        self.data_create_recipe_exists = {
            "recipe_name": "Recipe1",
            "recipe_text": "Recipe1 text.",
            "ingredients_list": ["Ing1", "Ing2", "Ing10"]
        }
        self.data_rate_recipe = {
            "recipe_name": "Recipe4",
            "recipe_rate": 5
        }
        self.data_rate_recipe_incomplete = {
            "recipe_name": "Recipe4",
        }
        self.data_rate_recipe_wrong = {
            "recipe_name": "Recipe4",
            "recipe_rate": "5"
        }
        self.data_rate_recipe_not_exists = {
            "recipe_name": "Recipe10",
            "recipe_rate": 5
        }
        self.data_rate_recipe_own = {
            "recipe_name": "Recipe1",
            "recipe_rate": 5
        }
        self.rate1 = Rate.objects.create(rate = 1)
        self.rate2 = Rate.objects.create(rate = 2)
        self.rate3 = Rate.objects.create(rate = 3)
        self.rate4 = Rate.objects.create(rate = 4)
        self.rate5 = Rate.objects.create(rate = 5)

        self.data_search = {
            "name": "1",
            "text": "3",
            "ingredients": ["Ing9"]
        }
        self.data_search_wrong = {
            "name": "1",
            "text": 1,
            "ingredients": [9]
        }
        self.data_filter = {
            "min_ingredients": 1,
            "max_ingredients": 4
        }
        self.data_filter_wrong = {
            "min_ingredients": 1,
            "max_ingredients": "4"
        }


    def test_create_recipe_POST(self, mock_user_detection):
        response = self.client.post(self.create_recipe_url, self.data_create_recipe, format="json")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("message" in response.data)
        self.assertTrue(Ingredient.objects.filter(name="Ing10").exists())


    def test_create_recipe_POST_incomplete_data(self, mock_user_detection):
        response = self.client.post(self.create_recipe_url, self.data_create_recipe_incomplete, format="json")
        
        self.assertRaises(ParseError)


    def test_create_recipe_POST_wrong_data_type(self, mock_user_detection):
        response = self.client.post(self.create_recipe_url, self.data_create_recipe_wrong, format="json")
        
        self.assertRaises(ParseError)


    def test_create_recipe_POST_already_exists(self, mock_user_detection):
        response = self.client.post(self.create_recipe_url, self.data_create_recipe_exists, format="json")
        
        self.assertRaises(ParseError)


    def test_all_recipes_GET(self, mock_user_detection):
        response = self.client.get(self.all_recipes_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["found_recipes"], 4)


    def test_my_recipes_GET(self, mock_user_detection):
        response = self.client.get(self.my_recipes_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["found_recipes"], 3)


    def test_rate_recipe_POST(self, mock_user_detection):
        response = self.client.post(self.rate_recipe_url, self.data_rate_recipe, format="json")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("message" in response.data)


    def test_rate_recipe_POST_incomplete_data(self, mock_user_detection):
        response = self.client.post(self.rate_recipe_url, self.data_rate_recipe_incomplete, format="json")

        self.assertRaises(ParseError)


    def test_rate_recipe_POST_wrong_data_type(self, mock_user_detection):
        response = self.client.post(self.rate_recipe_url, self.data_rate_recipe_wrong, format="json")

        self.assertRaises(ParseError)


    def test_rate_recipe_POST_recipe_does_not_exist(self, mock_user_detection):
        response = self.client.post(self.rate_recipe_url, self.data_rate_recipe_not_exists, format="json")

        self.assertRaises(ParseError)


    def test_rate_recipe_POST_rate_own_recipe(self, mock_user_detection):
        response = self.client.post(self.rate_recipe_url, self.data_rate_recipe_own, format="json")

        self.assertRaises(ParseError)


    def test_most_used_ingredients_GET(self, mock_user_detection):
        response = self.client.get(self.most_used_ingredients_url)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("most_used_ingredients" in response.data)


    def test_search_recipes_POST(self, mock_user_detection):
        response = self.client.post(self.search_recipes_url, self.data_search, format="json")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["found_recipes"], 3)


    def test_search_recipes_POST_wrong_data_type(self, mock_user_detection):
        response = self.client.post(self.search_recipes_url, self.data_search_wrong, format="json")

        self.assertRaises(ParseError)


    def test_filter_recipes_POST(self, mock_user_detection):
        response = self.client.post(self.filter_recipes_url, self.data_filter, format="json")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["found_recipes"], 2)


    def test_filter_recipes_POST_wrong_data_type(self, mock_user_detection):
        response = self.client.post(self.filter_recipes_url, self.data_filter_wrong, format="json")

        self.assertRaises(ParseError)
