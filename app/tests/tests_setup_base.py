from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth.models import User


class TestsSetUpBase(APITestCase):
    def register_user(self):
        base_url = reverse('account-create')
        user = {
            'username': 'username',
            'email': 'email1@email.email',
            'password': 'password',
        }
        self.client.post(base_url, user)
        user = User.objects.get(username='username')
        self.token = Token.objects.get(user=user)

    def get_key(self):
        return 'Token ' + self.token.key