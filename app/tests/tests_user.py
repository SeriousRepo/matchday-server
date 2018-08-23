from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from app.serializers import UserSerializer
from django.contrib.auth.models import User


class UserTestSetUp(APITestCase):
    first_user = {
        'username': 'username1',
        'email': 'email1@email1.email1',
        'password': 'password1',
    }
    second_user = {
        'username': 'username2',
        'email': 'email2@email2.email2',
        'password': 'password2',
    }
    url = reverse('users-list')
    register_url = reverse('account-create')

    def post_first_user(self):
        self.client.post(self.register_url, self.first_user)
        
    def post_both_users(self):
        self.client.post(self.register_url, self.first_user)
        self.client.post(self.register_url, self.second_user)
        

class CreateUserTest(APITestCase):
    url = reverse('account-create')
    first_user = {
        'username': 'username1',
        'email': 'email1@email1.email1',
        'password': 'password1',
    }
    second_user = {
        'username': 'username2',
        'email': 'email2@email2.email2',
        'password': 'password2',
    }

    def expect_correct_user(self, expected_user, current_user):
        self.assertEqual(expected_user['id'], current_user['id'])
        self.assertEqual(expected_user['username'], current_user['username'])
        self.assertEqual(expected_user['email'], current_user['email'])
        self.assertIsNotNone(current_user['token'])

    def test_create_user(self):
        response = self.client.post(self.url, self.first_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.first_user['id'] = 1
        self.expect_correct_user(self.first_user, response.data)
        response = self.client.post(self.url, self.second_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.second_user['id'] = 2
        self.expect_correct_user(self.second_user, response.data)


class ReadUserTest(UserTestSetUp):
    def setUp(self):
        self.post_both_users()

    def expect_correct_user(self, expected_user, current_user):
        self.assertEqual(expected_user['id'], current_user['id'])
        self.assertEqual(expected_user['username'], current_user['username'])

    def test_read_user_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.first_user['id'] = 1
        self.second_user['id'] = 2
        self.expect_correct_user(self.first_user, response.data[0])
        self.expect_correct_user(self.second_user, response.data[1])

    def test_read_single_user(self):
        self.first_user['id'] = 1
        self.second_user['id'] = 2
        response = self.client.get('/users/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expect_correct_user(self.first_user, response.data)
        response = self.client.get('/users/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expect_correct_user(self.second_user, response.data)


# TODO implement update and delete methods
"""class UpdateUserTest(UserTestSetUp):
    def setUp(self):
        self.second_model = User(pk=1, email='email2@email2.email2', date_joined=date(2015, 3, 11), rank_points=54321)
        self.second_user = UserSerializer(self.second_model).data
        self.post_first_user()

    def test_update_user(self):
        response = self.client.put('/users/{}/'.format(self.first_model.pk), self.second_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_user)
        response = self.client.get('/users/{}/'.format(self.first_model.pk))
        self.assertEqual(response.data, self.second_user)


class DeleteUserTest(UserTestSetUp):
    def setUp(self):
        self.post_both_users()

    def test_delete_user(self):
        response = self.client.delete('/users/{}/'.format(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.delete('/users/{}/'.format(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
"""