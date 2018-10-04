from rest_framework.reverse import reverse
from rest_framework import status
from app.models import Person
from app.tests.helpers.tests_setup_base import TestsSetUpBase
from app.tests.helpers.common_data import player_person, coach_person, referee_person, wrong_type_person


class PersonTestSetUp(TestsSetUpBase):
    base_url = reverse('people-list')
    person1 = coach_person(1)
    person2 = player_person(2)
    updated_person = referee_person(1)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)

    def post_single_person(self):
        self.register_user()
        self.post_method(self.base_url, self.person1.json)

    def post_two_persons(self):
        self.register_user()
        self.post_method(self.base_url, self.person1.json)
        self.post_method(self.base_url, self.person2.json)


class CreatePersonTest(PersonTestSetUp):
    def setUp(self):
        self.register_user()

    def test_create_person(self):
        response = self.post_method(self.base_url, self.person1.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.get(pk=1), self.person1.model)
        response = self.post_method(self.base_url, self.person2.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 2)
        self.assertEqual(Person.objects.get(pk=2), self.person2.model)

    def test_not_create_person_with_wrong_role(self):
        wrong_role_person = wrong_type_person(1)
        response = self.post_method(self.base_url, wrong_role_person.json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Person.objects.count(), 0)


class ReadPersonTest(PersonTestSetUp):
    def setUp(self):
        self.post_two_persons()

    def test_read_person_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.person1.json)
        self.assertEqual(response.data[1], self.person2.json)

    def test_read_single_person(self):
        response = self.get_method(self.get_nth_element_url(self.person1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.person1.json)
        response = self.get_method(self.get_nth_element_url(self.person2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.person2.json)


class UpdatePersonTest(PersonTestSetUp):
    def setUp(self):
        self.post_single_person()

    def test_update_person(self):
        response = self.put_method(self.get_nth_element_url(self.person1.model.pk), self.updated_person.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.updated_person.json)
        self.assertEqual(Person.objects.get(pk=1), self.updated_person.model)


class DeletePersonTest(PersonTestSetUp):
    def setUp(self):
        self.post_two_persons()

    def test_delete_person(self):
        response = self.delete_method(self.get_nth_element_url(self.person1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.person2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)


class PermissionsTest(PersonTestSetUp):
    def setUp(self):
        self.post_two_persons()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.person1.model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        response = self.client.post(self.base_url, self.person1.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.person1.model.pk), self.updated_person.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.person1.model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
