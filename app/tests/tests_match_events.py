from rest_framework.reverse import reverse
from rest_framework import status
from app.models import MatchEvent
from app.tests.helpers.tests_setup_base import TestsSetUpBase
from app.tests.helpers.data_representations import MatchEventRepresentation
from app.tests.helpers.common_data import match, event_info, referee_person, league_competition


class MatchEventTestSetUp(TestsSetUpBase):
    base_url = reverse('match_events-list')
    referee = referee_person(1)
    competition = league_competition(1)
    match1 = match(1)
    #match2 = match(2)

    def create_events(self):
        self.register_user(2)
        self.event_info1 = event_info(1, self.get_user_model(2))
        self.event_info2 = event_info(2, self.get_user_model(2))
        self.match_event1 = MatchEventRepresentation(1, self.match1.model, self.event_info1.model)
        self.match_event2 = MatchEventRepresentation(2, self.match1.model, self.event_info2.model)

    def post_nested_to_single(self):
        self.register_user()
        self.create_events()
        self.post_method(reverse('people-list'), self.referee.json)
        self.post_method(reverse('competitions-list'), self.competition.json)
        self.post_method(reverse('matches-list'), self.match1.json)
        
    def post_nested_to_both(self):
        self.register_user()
        self.post_nested_to_single()

    def post_single_match(self):
        self.post_nested_to_single()
        self.post_method(self.base_url, self.match_event1.json)

    def post_two_matches(self):
        self.post_nested_to_both()
        self.post_method(self.base_url, self.match_event1.json)
        self.post_method(self.base_url, self.match_event2.json)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)


class CreateMatchTest(MatchEventTestSetUp):
    def setUp(self):
        self.post_nested_to_both()

    def test_create_match(self):
        response = self.post_method(self.base_url, self.match_event1.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MatchEvent.objects.count(), 1)
        self.assertEqual(response.data, self.match_event1.json)
        response = self.post_method(self.base_url, self.match_event2.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MatchEvent.objects.count(), 2)
        self.assertEqual(response.data, self.match_event2.json)


"""class WrongCreationOfMatchEventTest(MatchEventTestSetUp):
    def setUp(self):
        self.post_nested_to_single(self.referee)

    def test_not_create_match_team_when_non_coach_person_type(self):
        non_coach_match_team = MatchEventRepresentation(1, self.team.model, self.match1.model, self.referee.model)
        response = self.post_method(self.base_url, non_coach_match_team.json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    #TODO
    #def test_not_create_two_match_team_with_same_matches_and_teams(self):


class ReadMatchTest(MatchEventTestSetUp):
    def setUp(self):
        self.post_two_matches()

    def test_read_match_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.match_team1.json)
        self.assertEqual(response.data[1], self.match_team2.json)

    def test_read_single_match(self):
        response = self.get_method(self.get_nth_element_url(self.match_team1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.match_team1.json)
        response = self.get_method(self.get_nth_element_url(self.match_team2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.match_team2.json)


class UpdateMatchTest(MatchEventTestSetUp):
    def setUp(self):
        self.post_nested_to_both()
        self.post_method(self.base_url, self.match_team1.json)

    def test_update_match(self):
        response = self.put_method(self.get_nth_element_url(self.match1.model.pk), self.updated_match_team.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.updated_match_team.json)
        response = self.get_method(self.get_nth_element_url(self.match1.model.pk))
        self.assertEqual(response.data, self.updated_match_team.json)


class DeleteMatchTest(MatchEventTestSetUp):
    def setUp(self):
        self.post_two_matches()

    def test_delete_match(self):
        response = self.delete_method(self.get_nth_element_url(self.match_team1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MatchEvent.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.match_team2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MatchEvent.objects.count(), 0)


class PermissionsTest(MatchEventTestSetUp):
    def setUp(self):
        self.post_two_matches()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.match_team1.model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        response = self.client.post(self.base_url, self.match_team1.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.match_team1.model.pk), self.updated_match_team.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.match_team1.model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
"""