from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from app.models import Person
from app.serializers import PersonSerializer
from datetime import date


class PersonTestSetUp(APITestCase):
    first_model = Person(pk=1, last_name='LastName1', first_name='FirstName1',
                         role='coach', birth_date=date(1961, 5, 13), nationality='French')
    first_person = PersonSerializer(first_model).data
    second_model = Person(pk=2, last_name='LastName2', first_name='FirstName2',
                          role='player', birth_date=date(1979, 1, 12), nationality='Polish')
    second_person = PersonSerializer(second_model).data
    url = reverse('people-list')

    def register_user(self):
        url = reverse('account-create')
        user = {
            'username': 'username',
            'email': 'email1@email.email',
            'password': 'password',
        }
        self.client.post(url, user, format='json')
        user = User.objects.get(username='username')
        self.token = Token.objects.get(user=user)

    def post_first_person(self):
        self.register_user()
        self.client.post(self.url, self.first_person, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)

    def post_both_persons(self):
        self.register_user()
        self.client.post(self.url, self.first_person, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.post(self.url, self.second_person, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)


class CreatePersonTest(PersonTestSetUp):
    def setUp(self):
        self.register_user()

    def test_create_person(self):
        response = self.client.post(self.url, self.first_person, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.get(pk=1), self.first_model)
        response = self.client.post(self.url, self.second_person, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 2)
        self.assertEqual(Person.objects.get(pk=2), self.second_model)

    def test_not_create_person_with_wrong_role(self):
        first_model = Person(pk=1, last_name='LastName1', first_name='FirstName1',
                             role='WrongRole', birth_date=date(1961, 5, 13))
        first_person = PersonSerializer(first_model).data
        response = self.client.post(self.url, first_person, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Person.objects.count(), 0)


class ReadPersonTest(PersonTestSetUp):
    def setUp(self):
        self.post_both_persons()

    def test_read_person_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.first_person)
        self.assertEqual(response.data[1], self.second_person)

    def test_read_single_person(self):
        response = self.client.get('/people/{}/'.format(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.first_person)
        response = self.client.get('/people/{}/'.format(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_person)


class UpdatePersonTest(PersonTestSetUp):
    def setUp(self):
        self.second_model = Person(pk=1, last_name='LastName2', first_name='FirstName2',
                                   role='player', birth_date=date(1979, 1, 12), nationality='Polish')
        self.second_person = PersonSerializer(self.second_model).data
        self.post_first_person()

    def test_update_person(self):
        response = self.client.put('/people/{}/'.format(self.first_model.pk), self.second_person, HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_person)
        response = self.client.get('/people/{}/'.format(self.first_model.pk))
        self.assertEqual(response.data, self.second_person)


class DeletePersonTest(PersonTestSetUp):
    def setUp(self):
        self.post_both_persons()

    def test_delete_person(self):
        response = self.client.delete('/people/{}/'.format(self.first_model.pk), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 1)
        response = self.client.delete('/people/{}/'.format(self.second_model.pk), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)


class PermissionsTest(PersonTestSetUp):
    def setUp(self):
        self.post_both_persons()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get('{}{}/'.format(self.url, self.first_model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        updated_person = self.first_person.copy()
        updated_person['nationality'] = 'changed_nationality'

        response = self.client.post(self.url, self.first_person)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put('{}{}/'.format(self.url, self.first_model.pk), updated_person)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete('{}{}/'.format(self.url, self.first_model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
