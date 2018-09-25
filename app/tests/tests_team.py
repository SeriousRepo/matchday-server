from rest_framework.reverse import reverse
from rest_framework import status
from app.models import Team
from app.tests.tests_setup_base import TestsSetUpBase
from app.tests.data_representations import TeamRepresentation


class TeamTestSetUp(TestsSetUpBase):
    base_url = reverse('teams-list')
    team1 = TeamRepresentation(1)
    team2 = TeamRepresentation(2)
    updated_team = TeamRepresentation(1, 'updated_city')
    
    def post_single_team(self):
        self.register_user()
        self.post_method(self.base_url, self.team1.json)

    def post_two_teams(self):
        self.register_user()
        self.post_method(self.base_url, self.team1.json)
        self.post_method(self.base_url, self.team2.json)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)
    

class CreateTeamTest(TeamTestSetUp):
    def setUp(self):
        self.register_user()

    def test_create_team(self):
        response = self.post_method(self.base_url, self.team1.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get(pk=1), self.team1.model)
        response = self.post_method(self.base_url, self.team2.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)
        self.assertEqual(Team.objects.get(pk=2), self.team2.model)


class ReadTeamTest(TeamTestSetUp):
    def setUp(self):
        self.post_two_teams()

    def test_read_team_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.team1.json)
        self.assertEqual(response.data[1], self.team2.json)

    def test_read_single_team(self):
        response = self.get_method(self.get_nth_element_url(self.team1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.team1.json)
        response = self.get_method(self.get_nth_element_url(self.team2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.team2.json)


class UpdateTeamTest(TeamTestSetUp):
    def setUp(self):
        self.post_single_team()

    def test_update_team(self):
        response = self.put_method(self.get_nth_element_url(self.team1.model.pk), self.updated_team.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.updated_team.json)
        self.assertEqual(Team.objects.get(pk=1), self.updated_team.model)


class DeleteTeamTest(TeamTestSetUp):
    def setUp(self):
        self.post_two_teams()

    def test_delete_team(self):
        response = self.delete_method(self.get_nth_element_url(self.team1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.team2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)


class PermissionsTest(TeamTestSetUp):
    def setUp(self):
        self.post_two_teams()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.team1.model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        response = self.client.post(self.base_url, self.team1.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.team1.model.pk), self.updated_team.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.team1.model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
