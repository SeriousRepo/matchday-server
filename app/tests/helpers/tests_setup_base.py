from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth.models import User


class TestsSetUpBase(APITestCase):
    def register_user(self, user_id=1):
        base_url = reverse('account-create')
        user = self.get_user_json(user_id)
        self.client.post(base_url, user)

    def get_user_json(self, user_id=1):
        return {
            'username': 'username' + str(user_id),
            'email': 'email1@email.email' + str(user_id),
            'password': 'password',
        }

    def get_user_model(self, user_id=1):
        return User.objects.get(username=self.get_user_json(user_id)['username'])

    def get_key(self, user_id=1):
        user = self.get_user_model(user_id)
        return 'Token ' + Token.objects.get(user=user).key

    def get_specific_url(self, base_url, n):
        return '{}{}/'.format(base_url, n)

    def get_method(self, url, user_id=1):
        return self.client.get(url, HTTP_AUTHORIZATION=self.get_key(user_id))

    def post_method(self, url, data, user_id=1):
        return self.client.post(url, data, HTTP_AUTHORIZATION=self.get_key(user_id), format='json')

    def put_method(self, url, data, user_id=1):
        return self.client.put(url, data, HTTP_AUTHORIZATION=self.get_key(user_id), format='json')

    def delete_method(self, url, user_id=1):
        return self.client.delete(url, HTTP_AUTHORIZATION=self.get_key(user_id))
