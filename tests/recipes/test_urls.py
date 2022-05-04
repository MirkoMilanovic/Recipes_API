from django.test import SimpleTestCase
from django.urls import reverse, resolve
from recipes.views import CreateRecipeView, AllRecipesView, MyRecipesView, RateRecipeView, MostUsedIngredientsView, SearchRecipesView, FilterRecipesView


class TestUrls(SimpleTestCase):

    def test_create_recipe_url(self):
        url = reverse('create_recipe')
        self.assertEquals(resolve(url).func.view_class, CreateRecipeView)


    def test_all_recipes_url(self):
        url = reverse('all_recipes')
        self.assertEquals(resolve(url).func.view_class, AllRecipesView)


    def test_my_recipes_url(self):
        url = reverse('my_recipes')
        self.assertEquals(resolve(url).func.view_class, MyRecipesView)

    
    def test_rate_recipe_url(self):
        url = reverse('rate_recipe')
        self.assertEquals(resolve(url).func.view_class, RateRecipeView)


    def test_most_used_ingredients_url(self):
        url = reverse('most_used_ingredients')
        self.assertEquals(resolve(url).func.view_class, MostUsedIngredientsView)


    def test_search_recipes_url(self):
        url = reverse('search_recipes')
        self.assertEquals(resolve(url).func.view_class, SearchRecipesView)


    def test_filter_recipes_url(self):
        url = reverse('filter_recipes')
        self.assertEquals(resolve(url).func.view_class, FilterRecipesView)