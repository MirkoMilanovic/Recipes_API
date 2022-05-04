from rest_framework.views import APIView
from users.models import User
from rest_framework.response import Response
from .models import Ingredient, Recipe, Rating, Rate
from .user_detection import user_detection
from .list_recipes import list_recipes
from rest_framework.exceptions import AuthenticationFailed, ParseError
from django.db.models import Q, Count
import operator
from functools import reduce


class CreateRecipeView(APIView):
    def post(self, request):
        try:
            recipe_name = request.data['recipe_name']
            recipe_text = request.data['recipe_text']
            ingredients_list = request.data['ingredients_list']
        except:
            raise ParseError('You should provide: recipe_name (str), recipe_text (str) and ingredients_list (list(str))!')

        if not isinstance(recipe_name, str) == isinstance(recipe_text, str) == isinstance(ingredients_list, list) == True or not all(isinstance(ing, str) for ing in ingredients_list):
            raise ParseError('Make sure that: recipe_name (type=str), recipe_text (type=str) and ingredients_list (type=list(str))!')

        user = User.objects.get(id=user_detection(request))

        try:
            recipe = Recipe(name=recipe_name, recipe_text=recipe_text, user=user)
            recipe.save()
        except:
            raise ParseError('The recipe with given name already exists!', code=300)

        for ingredient_name in ingredients_list:
            ingredient = Ingredient(name=ingredient_name.capitalize())
            ingredient = Ingredient.objects.get_or_create(name=ingredient_name.capitalize())[0]
            recipe.ingredients.add(ingredient)
            
        resp = {
            "status": 200, 
            "message": "Recipe created successfully!"
        }
        return Response(resp)


class AllRecipesView(APIView):
    def get(self, request):

        if not user_detection(request):
            raise AuthenticationFailed('Unauthenticated!')

        all_recipes_query = Recipe.objects.all()

        content = list_recipes(all_recipes_query)

        return Response(content)


class MyRecipesView(APIView):
    def get(self, request):

        my_recipes_query = Recipe.objects.all().filter(user=user_detection(request))
        
        content = list_recipes(my_recipes_query)

        return Response(content)


class RateRecipeView(APIView):
    def post(self, request):
        try:
            recipe_name = request.data['recipe_name']
            recipe_rate = request.data['recipe_rate']
        except:
            raise ParseError('You should provide: recipe_name (str) and recipe_rate (int(1-5))!')

        if not isinstance(recipe_name, str) == True or recipe_rate not in [1,2,3,4,5]:
            raise ParseError('Make sure that: recipe_name (type=str) and recipe_rate (type=int(1-5)!')

        recipe = Recipe.objects.filter(name=recipe_name).first()
        
        if not recipe:
            raise ParseError("This recipe does not exist!")

        if recipe.user_id == user_detection(request):
            raise ParseError('You cannot rate your own recipe!')

        user = User.objects.filter(id=user_detection(request)).first()
        rate = Rate.objects.filter(id=recipe_rate).first()

        Rating.objects.update_or_create(user=user, recipe=recipe, defaults = {'rate': rate})
        resp = {
            "status": 200, 
            "message": "Recipe rated successfully!"
        }
        return Response(resp)


class MostUsedIngredientsView(APIView):
    def get(self, request):
        if not user_detection(request):
            raise AuthenticationFailed('Unauthenticated!')

        ingredients_query = Recipe.objects.values_list('ingredients__name').annotate(count=Count('ingredients')).order_by('-count')[:5]

        most_used = []

        for ing in ingredients_query:
            most_used.append(ing[0])

        resp = {
            "status": 200, 
            "most_used_ingredients": most_used
        }
        return Response(resp)


class SearchRecipesView(APIView):
    def post(self, request):
        if not user_detection(request):
            raise AuthenticationFailed('Unauthenticated!')

        name = request.data.get("name", "xxxxx")
        text = request.data.get("text", "xxxxx")
        ingredients = request.data.get("ingredients", ["xxxxx"])

        if not isinstance(name, str) == isinstance(text, str) == isinstance(ingredients, list) == True or not all(isinstance(ing, str) for ing in ingredients):
            raise ParseError('Make sure that: name (type=str), text (type=str) and ingredients (type=list(str))!')

        recipes_found_query = Recipe.objects.filter(Q(name__icontains=name) | Q(recipe_text__icontains=text) | reduce(operator.or_, (Q(ingredients__name__icontains=ing) for ing in ingredients))).distinct()

        content = list_recipes(recipes_found_query)

        return Response(content)


class FilterRecipesView(APIView):
    def post(self, request):
        if not user_detection(request):
            raise AuthenticationFailed('Unauthenticated!')

        min_ingredients = request.data.get("min_ingredients", 0)
        max_ingredients = request.data.get("max_ingredients", 100)

        if not isinstance(min_ingredients, int) == isinstance(max_ingredients, int) == True:
            raise ParseError('Make sure that: min_ingredients (type=int) and max_ingredients (type=int)!')

        recipes_filtered_query = Recipe.objects.annotate(number_of_ingredients=Count('ingredients')).filter(number_of_ingredients__lte=max_ingredients, number_of_ingredients__gte=min_ingredients)

        content = list_recipes(recipes_filtered_query)

        return Response(content)