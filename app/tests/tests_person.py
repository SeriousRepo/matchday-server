from rest_framework.reverse import reverse
from rest_framework import status
from app.models import Person
from app.serializers import PersonSerializer
from datetime import date
from app.tests.tests_setup_base import TestsSetUpBase


class PersonTestSetUp(TestsSetUpBase):
    first_model = Person(pk=1, last_name='LastName1', first_name='FirstName1',
                         role='coach', birth_date=date(1961, 5, 13), nationality='French')
    first_person = PersonSerializer(first_model).data
    second_model = Person(pk=2, last_name='LastName2', first_name='FirstName2',
                          role='player', birth_date=date(1979, 1, 12), nationality='Polish')
    second_person = PersonSerializer(second_model).data
    base_url = reverse('people-list')

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)

    def post_first_person(self):
        self.register_user()
        self.post_method(self.base_url, self.first_person)

    def post_both_persons(self):
        self.register_user()
        self.post_method(self.base_url, self.first_person)
        self.post_method(self.base_url, self.second_person)


class CreatePersonTest(PersonTestSetUp):
    def setUp(self):
        self.register_user()

    def test_create_person(self):
        response = self.post_method(self.base_url, self.first_person)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.get(pk=1), self.first_model)
        response = self.post_method(self.base_url, self.second_person)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 2)
        self.assertEqual(Person.objects.get(pk=2), self.second_model)

    def test_not_create_person_with_wrong_role(self):
        first_model = Person(pk=1, last_name='LastName1', first_name='FirstName1',
                             role='WrongRole', birth_date=date(1961, 5, 13))
        first_person = PersonSerializer(first_model).data
        response = self.post_method(self.base_url, first_person)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Person.objects.count(), 0)


class ReadPersonTest(PersonTestSetUp):
    def setUp(self):
        self.post_both_persons()

    def test_read_person_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.first_person)
        self.assertEqual(response.data[1], self.second_person)

    def test_read_single_person(self):
        response = self.get_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.first_person)
        response = self.get_method(self.get_nth_element_url(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_person)


class UpdatePersonTest(PersonTestSetUp):
    def setUp(self):
        self.second_model = Person(pk=1, last_name='LastName2', first_name='FirstName2',
                                   role='player', birth_date=date(1979, 1, 12), nationality='Polish')
        self.second_person = PersonSerializer(self.second_model).data
        self.post_first_person()

    def test_update_person(self):
        response = self.put_method(self.get_nth_element_url(self.first_model.pk), self.second_person)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_person)
        response = self.get_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(response.data, self.second_person)


class DeletePersonTest(PersonTestSetUp):
    def setUp(self):
        self.post_both_persons()

    def test_delete_person(self):
        response = self.delete_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)


class PermissionsTest(PersonTestSetUp):
    def setUp(self):
        self.post_both_persons()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        updated_person = self.first_person.copy()
        updated_person['nationality'] = 'changed_nationality'

        response = self.client.post(self.base_url, self.first_person)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.first_model.pk), updated_person)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
