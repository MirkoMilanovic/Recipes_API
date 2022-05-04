from users.serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from RecipesAPI.constants import JWT_KEY
import jwt
from users.models import User


def user_detection(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)

    user_id = serializer.data['id']

    return user_id