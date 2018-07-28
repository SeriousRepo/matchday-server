from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Person
from app.serializers import PersonSerializer
from datetime import date


class PersonTestSetUp(APITestCase):
    first_model = Person(pk=1, last_name='LastName1', first_name='FirstName1',
                         role='coach', birth_date=date(1961, 5, 13))
    first_person = PersonSerializer(first_model).data
    second_model = Person(pk=2, last_name='LastName2', first_name='FirstName2',
                          role='player', birth_date=date(1979, 1, 12))
    second_person = PersonSerializer(second_model).data
    url = reverse('people-list')

    def post_first_person(self):
        self.client.post(self.url, self.first_person, format='json')

    def post_both_persons(self):
        self.client.post(self.url, self.first_person, format='json')
        self.client.post(self.url, self.second_person, format='json')


class CreatePersonTest(PersonTestSetUp):
    def test_create_person(self):
        response = self.client.post(self.url, self.first_person, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.get(pk=1), self.first_model)
        response = self.client.post(self.url, self.second_person, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 2)
        self.assertEqual(Person.objects.get(pk=2), self.second_model)

    def test_not_create_with_wrong_role(self):
        first_model = Person(pk=1, last_name='LastName1', first_name='FirstName1',
                             role='WrongRole', birth_date=date(1961, 5, 13))
        first_person = PersonSerializer(first_model).data
        response = self.client.post(self.url, first_person, format='json')
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
                                   role='player', birth_date=date(1979, 1, 12))
        self.second_person = PersonSerializer(self.second_model).data
        self.post_first_person()

    def test_update_person(self):
        response = self.client.put('/people/{}/'.format(self.first_model.pk), self.second_person)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_person)
        response = self.client.get('/people/{}/'.format(self.first_model.pk))
        self.assertEqual(response.data, self.second_person)


class DeletePersonTest(PersonTestSetUp):
    def setUp(self):
        self.post_both_persons()

    def test_delete_person(self):
        response = self.client.delete('/people/{}/'.format(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 1)
        response = self.client.delete('/people/{}/'.format(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)
