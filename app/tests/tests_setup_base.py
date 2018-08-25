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

    def get_specific_url(self, base_url, n):
        return '{}{}/'.format(base_url, n)

    def get_method(self, url):
        return self.client.get(url, HTTP_AUTHORIZATION=self.get_key())

    def post_method(self, url, data):
        return self.client.post(url, data, HTTP_AUTHORIZATION=self.get_key())

    def put_method(self, url, data):
        return self.client.put(url, data, HTTP_AUTHORIZATION=self.get_key())

    def delete_method(self, url):
        return self.client.delete(url, HTTP_AUTHORIZATION=self.get_key())
