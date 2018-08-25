from rest_framework.reverse import reverse
from rest_framework import status
from app.models import Competition
from app.serializers import CompetitionSerializer
from app.tests.tests_setup_base import TestsSetUpBase


# ToDo add tests for /competition/<id>/matches/ endpoint

class CompetitionTestSetUp(TestsSetUpBase):
    first_model = Competition(pk=1, name='Name1', type='league')
    first_competition = CompetitionSerializer(first_model).data
    second_model = Competition(pk=2, name='Name2', type='tournament')
    second_competition = CompetitionSerializer(second_model).data
    base_url = reverse('competitions-list')

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)

    def post_single_competition(self):
        self.register_user()
        self.post_method(self.base_url, self.first_competition)

    def post_both_competitions(self):
        self.register_user()
        self.post_method(self.base_url, self.first_competition)
        self.post_method(self.base_url, self.second_competition)


class CreateCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.register_user()

    def test_create_competition(self):
        response = self.post_method(self.base_url, self.first_competition)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competition.objects.count(), 1)
        self.assertEqual(Competition.objects.get(pk=1), self.first_model)
        response = self.post_method(self.base_url, self.second_competition)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competition.objects.count(), 2)
        self.assertEqual(Competition.objects.get(pk=2), self.second_model)

    def test_not_create_competition_with_wrong_type(self):
        first_model = Competition(pk=1, name='Name1', type='WrongType')
        first_person = CompetitionSerializer(first_model).data
        response = self.post_method(self.base_url, first_person)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Competition.objects.count(), 0)


class ReadCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_both_competitions()

    def test_read_competition_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.first_competition)
        self.assertEqual(response.data[1], self.second_competition)

    def test_read_single_competition(self):
        response = self.get_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.first_competition)
        response = self.get_method(self.get_nth_element_url(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_competition)


class UpdateCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.second_model = Competition(pk=1, name='Name2', type='tournament')
        self.second_competition = CompetitionSerializer(self.second_model).data
        self.post_single_competition()

    def test_update_competition(self):
        response = self.put_method(self.get_nth_element_url(self.first_model.pk), self.second_competition)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_competition)
        response = self.get_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(response.data, self.second_competition)


class DeleteCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_both_competitions()

    def test_delete_competition(self):
        response = self.delete_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Competition.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Competition.objects.count(), 0)


class PermissionsTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_both_competitions()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        updated_competition = self.first_competition.copy()
        updated_competition['name'] = 'changed_name'

        response = self.client.post(self.base_url, self.first_competition)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.first_model.pk), updated_competition)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
