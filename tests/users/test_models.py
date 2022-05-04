from django.test import TestCase
from users.models import User


class TestModels(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email = 'petar@m.com',
            first_name = "Petar",
            last_name = "Petrovic",
            password = 'petar123',
        )


    def test_user(self):
        self.assertEquals(self.user1.first_name, "Petar")
