from rest_framework.reverse import reverse
from rest_framework import status
from app.models import Competition
from app.tests.helpers.tests_setup_base import TestsSetUpBase
from app.tests.helpers.common_data import tournament_competition, league_competition, wrong_type_competition


# ToDo add tests for /competition/<id>/matches/ endpoint

class CompetitionTestSetUp(TestsSetUpBase):
    base_url = reverse('competitions-list')
    competition1 = league_competition(1)
    competition2 = tournament_competition(2)
    updated_competition = tournament_competition(1)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)

    def post_single_competition(self):
        self.register_user()
        self.post_method(self.base_url, self.competition1.json)

    def post_two_competitions(self):
        self.register_user()
        self.post_method(self.base_url, self.competition1.json)
        self.post_method(self.base_url, self.competition2.json)


class CreateCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.register_user()

    def test_create_competition(self):
        response = self.post_method(self.base_url, self.competition1.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competition.objects.count(), 1)
        self.assertEqual(Competition.objects.get(pk=1), self.competition1.model)
        response = self.post_method(self.base_url, self.competition2.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competition.objects.count(), 2)
        self.assertEqual(Competition.objects.get(pk=2), self.competition2.model)

    def test_not_create_competition_with_wrong_type(self):
        wrong_competition = wrong_type_competition(1)
        response = self.post_method(self.base_url, wrong_competition.json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Competition.objects.count(), 0)


class ReadCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_two_competitions()

    def test_read_competition_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.competition1.json)
        self.assertEqual(response.data[1], self.competition2.json)

    def test_read_single_competition(self):
        response = self.get_method(self.get_nth_element_url(self.competition1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.competition1.json)
        response = self.get_method(self.get_nth_element_url(self.competition2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.competition2.json)


class UpdateCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_single_competition()

    def test_update_competition(self):
        response = self.put_method(self.get_nth_element_url(self.competition1.model.pk), self.updated_competition.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.updated_competition.json)
        response = self.get_method(self.get_nth_element_url(self.competition1.model.pk))
        self.assertEqual(response.data, self.updated_competition.json)


class DeleteCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_two_competitions()

    def test_delete_competition(self):
        response = self.delete_method(self.get_nth_element_url(self.competition1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Competition.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.competition2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Competition.objects.count(), 0)


class PermissionsTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_two_competitions()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.competition1.model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        response = self.client.post(self.base_url, self.competition1.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.competition1.model.pk), self.updated_competition.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.competition1.model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
