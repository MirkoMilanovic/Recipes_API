import requests
from rest_framework.exceptions import ValidationError
from RecipesAPI.constants import HUNTER_API_KEY, CLEARBIT_API_KEY
import clearbit


def email_validation(email):
    detected = False
    apiUrl = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}'

    response = requests.get(apiUrl)

    result = response.json()
    if result['data']['status'] not in ['verified', 'accept_all', 'webmail']:
        raise ValidationError({'message': 'This email is not valid!'})
    
    detected = True

    return detected


def clearbit_info(email):
    clearbit.key = CLEARBIT_API_KEY

    clearbit_data =  clearbit.Person.find(email=email)

    return clearbit_data