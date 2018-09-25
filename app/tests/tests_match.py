from rest_framework.reverse import reverse
from rest_framework import status
from app.models import Match
from app.tests.tests_setup_base import TestsSetUpBase
from app.tests.data_representations import PersonRepresentation, CompetitionRepresentation, MatchRepresentation


class MatchTestSetUp(TestsSetUpBase):
    base_url = reverse('matches-list')
    referee = PersonRepresentation(1, 'referee')
    competition1 = CompetitionRepresentation(1, 'league')
    competition2 = CompetitionRepresentation(2, 'tournament')
    match1 = MatchRepresentation(1, referee.model, competition1.model)
    match2 = MatchRepresentation(2, referee.model, competition2.model)
    updated_match = MatchRepresentation(1, referee.model, competition2.model)

    def post_nested(self, person=referee):
        self.register_user()
        self.post_method(reverse('people-list'), person.json)
        self.post_method(reverse('competitions-list'), self.competition1.json)
        self.post_method(reverse('competitions-list'), self.competition2.json)

    def post_single_match(self):
        self.post_nested()
        self.post_method(self.base_url, self.match1.json)

    def post_two_matches(self):
        self.post_nested()
        self.post_method(self.base_url, self.match1.json)
        self.post_method(self.base_url, self.match2.json)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)


class CreateMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()

    def test_create_match(self):
        response = self.post_method(self.base_url, self.match1.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(response.data, self.match1.json)
        response = self.post_method(self.base_url, self.match2.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 2)
        self.assertEqual(response.data, self.match2.json)


class WrongCreationOfMatchTest(MatchTestSetUp):
    def setUp(self):
        self.coach = PersonRepresentation(1, 'coach')
        self.register_user()
        self.post_method(reverse('people-list'), self.coach.json)
        self.post_method(reverse('competitions-list'), self.competition1.json)

    def test_not_create_match_when_non_referee_person_type(self):
        non_referee_match = MatchRepresentation(1, self.coach.model, self.competition1.model)
        response = self.post_method(self.base_url, non_referee_match.json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class ReadMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_two_matches()

    def test_read_match_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.match1.json)
        self.assertEqual(response.data[1], self.match2.json)

    def test_read_single_match(self):
        response = self.get_method(self.get_nth_element_url(self.match1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.match1.json)
        response = self.get_method(self.get_nth_element_url(self.match2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.match2.json)


class UpdateMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_single_match()

    def test_update_match(self):
        response = self.put_method(self.get_nth_element_url(self.match1.model.pk), self.updated_match.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.updated_match.json)
        response = self.get_method(self.get_nth_element_url(self.match1.model.pk))
        self.assertEqual(response.data, self.updated_match.json)


class DeleteMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_two_matches()

    def test_delete_match(self):
        response = self.delete_method(self.get_nth_element_url(self.match1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Match.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.match2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Match.objects.count(), 0)


class PermissionsTest(MatchTestSetUp):
    def setUp(self):
        self.post_two_matches()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.match1.model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        response = self.client.post(self.base_url, self.match1.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.match1.model.pk), self.updated_match.json)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.match1.model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
