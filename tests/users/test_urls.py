from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import RegisterView, LoginView, UserView, LogoutView


class TestUrls(SimpleTestCase):

    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, RegisterView)


    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)


    def test_user_url(self):
        url = reverse('user')
        self.assertEquals(resolve(url).func.view_class, UserView)

    
    def test_logout_url(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)