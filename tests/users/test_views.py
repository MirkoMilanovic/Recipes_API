from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from users.views import RegisterView, LoginView, UserView, LogoutView
from rest_framework.exceptions import ValidationError
from http.cookies import SimpleCookie
from django.urls import reverse
from users.models import User
from users import views
import mock


@mock.patch.object(views, "email_validation", return_value=True)
@mock.patch.object(views, "clearbit_info", return_value="")
class TestViews(APITestCase):
    def setUp(self):
        
        self.factory = APIRequestFactory()

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_url = reverse('user')
        self.logout_url = reverse('logout')

        self.user1 = User.objects.create(
            email = "user1@stripe.com",
            first_name = "Name1",
            last_name = "Lastname1",
            password = "123"
        )
        self.user1.set_password('123')
        self.user1.save()

        self.data_user = {
            "email": "user@stripe.com",
            "first_name": "Name",
            "last_name": "Lastname",
            "password": "789"
        }
        self.data_user1 = {
            "email": "user1@stripe.com",
            "first_name": "Name1",
            "last_name": "Lastname1",
            "password": "123"
        }
        self.data_login = {
            "email": "user1@stripe.com",
            "password": "123"
        }


    def test_register_POST(self, mock_email_validation, mock_clearbit_info):
        request = self.factory.patch(self.register_url, format="json")
        request.data = self.data_user

        response = RegisterView().post(request)

        self.assertEquals(response.status_code, 200)


    def test_register_POST_user_exists(self, mock_email_validation, mock_clearbit_info):
        response = APIClient().post(self.register_url, self.data_user1, format="json")

        self.assertRaises(ValidationError)


    def test_login_POST_and_user_GET(self, mock_email_validation, mock_clearbit_info):
        request  = self.factory.patch(self.login_url, format="json")
        request.data = self.data_login
        response = LoginView().post(request)
        token = response.data['jwt']

        self.assertEquals(response.status_code, 200)
        self.assertTrue("jwt" in response.data)

        self.factory.cookies = SimpleCookie({'jwt': token})
        request  = self.factory.get(self.user_url)

        response = UserView().get(request)

        self.assertEquals(response.status_code, 200)


    def test_logout_GET(self, mock_email_validation, mock_clearbit_info):
        request  = self.factory.get(self.user_url)

        response = LogoutView().get(request)

        self.assertEquals(response.status_code, 200)