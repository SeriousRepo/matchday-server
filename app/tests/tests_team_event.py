from rest_framework.reverse import reverse
from rest_framework import status
from app.models import TeamEvent
from app.tests.helpers.tests_setup_base import TestsSetUpBase
from app.tests.helpers.data_representations import TeamEventRepresentation
from app.tests.helpers.common_data import match_team, event_info, player, team, match, coach_person, referee_person, league_competition


class TeamEventTestSetUp(TestsSetUpBase):
    base_url = reverse('team_events-list')
    player1 = player(1)
    match_team = match_team(1, coach_person(2), match(1, referee_person(3)))

    def create_events(self):
        self.register_user(2)
        self.event_info1 = event_info(1, self.get_user_model(2))
        self.event_info2 = event_info(2, self.get_user_model(2))
        self.team_event1 = TeamEventRepresentation(1, self.player1.model, self.match_team.model, self.event_info1.model)
        self.team_event2 = TeamEventRepresentation(2, self.player1.model, self.match_team.model, self.event_info2.model)
        self.updated_team_event = TeamEventRepresentation(1, self.player1.model, self.match_team.model, self.event_info2.model)

    def post_nested_to_single(self):
        self.register_user()
        self.create_events()
        self.post_method(reverse('teams-list'), team(1).json)
        self.post_method(reverse('players-list'), self.player1.json)
        self.post_method(reverse('people-list'), coach_person(2).json)
        self.post_method(reverse('people-list'), referee_person(3).json)
        self.post_method(reverse('competitions-list'), league_competition(1).json)
        self.post_method(reverse('matches-list'), match(1, referee_person(3)).json)
        self.post_method(reverse('match_teams-list'), self.match_team.json)

    def post_nested_to_both(self):
        self.post_nested_to_single()

    def post_single_match(self):
        self.post_nested_to_single()
        self.post_method(self.base_url, self.team_event1.json)

    def post_two_matches(self):
        self.post_nested_to_both()
        self.post_method(self.base_url, self.team_event1.json)
        self.post_method(self.base_url, self.team_event2.json)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)


class CreateMatchTest(TeamEventTestSetUp):
    def setUp(self):
        self.post_nested_to_both()

    def test_create_match(self):
        response = self.post_method(self.base_url, self.team_event1.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeamEvent.objects.count(), 1)
        self.assertEqual(response.data, self.team_event1.json)
        response = self.post_method(self.base_url, self.team_event2.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeamEvent.objects.count(), 2)
        self.assertEqual(response.data, self.team_event2.json)


# class WrongCreationOfTeamEventTest(TeamEventTestSetUp):
# Todo restrict adding same event several times
# def test_restrict_creating_same_player_several_times(self):


class ReadMatchTest(TeamEventTestSetUp):
    def setUp(self):
        self.post_two_matches()

    def test_read_match_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.team_event1.json)
        self.assertEqual(response.data[1], self.team_event2.json)

    def test_read_single_match(self):
        response = self.get_method(self.get_nth_element_url(self.team_event1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.team_event1.json)
        response = self.get_method(self.get_nth_element_url(self.team_event2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.team_event2.json)


"""
# ToDo fix nested
class UpdateMatchTest(TeamEventTestSetUp):
    def setUp(self):
        self.post_nested_to_both()
        self.post_method(self.base_url, self.team_event1.json)
        self.post_method(reverse('matches-list'), player(4).json)

    def test_update_match(self):
        response = self.put_method(self.get_nth_element_url(self.team_event1.model.pk), self.updated_team_event.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.updated_team_event.json)
        response = self.get_method(self.get_nth_element_url(self.team_event1.model.pk))
        self.assertEqual(response.data, self.updated_team_event.json)
"""

class DeleteMatchTest(TeamEventTestSetUp):
    def setUp(self):
        self.post_two_matches()

    def test_delete_match(self):
        response = self.delete_method(self.get_nth_element_url(self.team_event1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TeamEvent.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.team_event2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TeamEvent.objects.count(), 0)


class PermissionsTest(TeamEventTestSetUp):
    def setUp(self):
        self.post_two_matches()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.team_event1.model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        response = self.client.post(self.base_url, self.team_event1.json, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.team_event1.model.pk), self.updated_team_event.json, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.team_event1.model.pk), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)