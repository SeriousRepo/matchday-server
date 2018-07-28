from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import User
from app.serializers import UserSerializer
from datetime import date


class UserTestSetUp(APITestCase):
    first_model = User(pk=1, email='email1@email1.email1', join_date=date(2013, 5, 13), rank_points=12345)
    first_user = UserSerializer(first_model).data
    second_model = User(pk=2, email='email2@email2.email2', join_date=date(2015, 3, 11), rank_points=54321)
    second_user = UserSerializer(second_model).data
    url = reverse('users-list')

    def post_first_user(self):
        self.client.post(self.url, self.first_user, format='json')

    def post_both_users(self):
        self.client.post(self.url, self.first_user, format='json')
        self.client.post(self.url, self.second_user, format='json')
        

class CreateUserTest(UserTestSetUp):
    def test_create_user(self):
        response = self.client.post(self.url, self.first_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(pk=1), self.first_model)
        response = self.client.post(self.url, self.second_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(pk=2), self.second_model)


class ReadUserTest(UserTestSetUp):
    def setUp(self):
        self.post_both_users()

    def test_read_user_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.first_user)
        self.assertEqual(response.data[1], self.second_user)

    def test_read_single_user(self):
        response = self.client.get('/users/{}/'.format(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.first_user)
        response = self.client.get('/users/{}/'.format(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_user)


class UpdateUserTest(UserTestSetUp):
    def setUp(self):
        self.second_model = User(pk=1, email='email2@email2.email2', join_date=date(2015, 3, 11), rank_points=54321)
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
