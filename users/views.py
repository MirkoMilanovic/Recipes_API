from rest_framework.views import APIView
from RecipesAPI.constants import JWT_KEY
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError, ParseError
from .serializers import UserSerializer
from .models import User
from .external_api import email_validation, clearbit_info
import jwt, datetime


class RegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            name = request.data['first_name']
            last_name = request.data['last_name']
            password = request.data['password']
        except:
            raise ParseError('You should provide: email (str), first_name (str), last_name (str) and password (str)!')

        if not isinstance(email, str) == isinstance(name, str) == isinstance(last_name, str) == isinstance(password, str) == True:
            raise ParseError('Make sure that all data have type=str!')

        if not email_validation(email):
            raise ValidationError({'message': 'The email validation service is not available at the moment!'})

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        content = {
            'message': f'Welcome {name}! You have successfully registered!',
            'user': serializer.data
        }
        return Response(content)


class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
        except:
            raise ParseError('You should provide: email (str) and password (str)!')

        if not isinstance(email, str) == isinstance(password, str) == True:
            raise ParseError('Make sure that all data have type=str!')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, JWT_KEY, algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        email = serializer.data['email']
        
        person_clearbit = clearbit_info(email)
        content = {
            'user': serializer.data,
            'clearbit_info' : person_clearbit
        }
        return Response(content)


class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You have successfully logged out!'
        }
        return response