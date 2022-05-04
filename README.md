# Recipes API

This Django API is used for food recipes. JWT is used for user authentication. Hunter API is used
for email verification and Clearbit API for providing additional user information.

## Features:

| Method | Path                   | Parameter                   | Description               |
| ------ | ---------------------- | --------------------------- | ------------------------- |
| POST   | /auth/register         | email: Str                  | User registration         |
|        |                        | first_name: Str             |                           |
|        |                        | last_name: Str              |                           |
|        |                        | password: Str               |                           |
|        |                        |                             |                           |
| POST   | /auth/login            | email: Str                  | User registration         |
|        |                        | password: Str               |                           |
|        |                        |                             |                           |
| GET    | /auth/user             |                             | Get user information      |
|        |                        |                             |                           |
| GET    | /auth/logout           |                             | User logout               |
|        |                        |                             |                           |
| POST   | /create_recipe         | recipe_name: Str            | Recipe creation           |
|        |                        | recipe_text: Str            |                           |
|        |                        | ingredients_list: List(Str) |                           |
|        |                        |                             |                           |
| GET    | /all_recipes           |                             | List all recipes          |
|        |                        |                             |                           |
| GET    | /my_recipes            |                             | List own recipes          |
|        |                        |                             |                           |
| POST   | /rate_recipe           | recipe_name: Str            | Racipe rating (you cannot |
|        |                        | recipe_rate: Int (1-5)      | rate your own recipes)    |
|        |                        |                             |                           |
| GET    | /most_used_ingredients |                             | Get most used ingredients |
|        |                        |                             | (top 5)                   |
|        |                        |                             |                           |
| POST   | /search_recipes        | name: Str                   |                           |
|        |                        | ingredients: Str            |                           |
|        |                        |                             |                           |
| POST   | /filter_recipes        | min_ingredients: Int        |                           |
|        |                        | max_ingredients: Int        |                           |

### Requirements:

See requirements.txt

### Database setup

```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data_rate
```

### Test

Run tests with:

```
python manage.py test
```

### Docker

Run the API using Docker with:

```
sudo docker-compose build
sudo docker-compose up
```

### Note

The constants.py file with API and JWT keys is excluded. Make your own.
