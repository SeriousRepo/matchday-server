from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from datetime import date, datetime
from app.models import Match, Person, Competition
from app.serializers import MatchSerializer, PersonSerializer, CompetitionSerializer
from app.tests.tests_setup_base import TestsSetUpBase


# ToDo add more referees and competitions

class MatchTestSetUp(TestsSetUpBase):
    base_url = reverse('matches-list')
    url_prefix = {'request': APIRequestFactory().get('/')}
    first_referee_model = Person(pk=1, last_name='LastName1', first_name='FirstName1',
                                 role='referee', birth_date=date(1961, 5, 13))
    first_referee = PersonSerializer(first_referee_model).data
    first_competition_model = Competition(pk=1, name='Name1', type='league')
    first_competition = CompetitionSerializer(first_competition_model).data
    first_model = Match(pk=1, date=datetime(2018, 11, 10, 20, 45),
                        main_referee=first_referee_model, competition=first_competition_model)
    first_match = MatchSerializer(first_model, context=url_prefix).data
    second_model = Match(pk=2, date=datetime(2019, 1, 3, 20, 45),
                         main_referee=first_referee_model, competition=first_competition_model)
    second_match = MatchSerializer(second_model, context=url_prefix).data

    def post_nested(self):
        self.register_user()
        self.post_method(reverse('people-list'), self.first_referee)
        self.post_method(reverse('competitions-list'), self.first_competition)

    def post_first_match(self):
        self.register_user()
        self.post_method(self.base_url, self.first_match)

    def post_both_matches(self):
        self.register_user()
        self.post_method(self.base_url, self.first_match)
        self.post_method(self.base_url, self.second_match)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)


class CreateMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()

    def test_create_match(self):
        response = self.post_method(self.base_url, self.first_match)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(response.data, self.first_match)
        response = self.post_method(self.base_url, self.second_match)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 2)
        self.assertEqual(response.data, self.second_match)


class WrongCreationOfMatchTest(MatchTestSetUp):
    def setUp(self):
        self.first_referee['role'] = 'player'
        self.post_nested()

    def test_not_create_match_when_non_referee_person_type(self):
        response = self.post_method(self.base_url, self.first_match)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class ReadMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()
        self.post_both_matches()

    def test_read_match_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.first_match)
        self.assertEqual(response.data[1], self.second_match)

    def test_read_single_match(self):
        response = self.get_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.first_match)
        response = self.get_method(self.get_nth_element_url(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_match)


class UpdateMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()
        self.second_model = Match(pk=1, date=datetime(2019, 1, 3, 20, 45),
                                  main_referee=self.first_referee_model, competition=self.first_competition_model)
        self.second_match = MatchSerializer(self.second_model, context=self.url_prefix).data
        self.post_first_match()

    def test_update_match(self):
        response = self.put_method(self.get_nth_element_url(self.first_model.pk), self.second_match)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_match)
        response = self.get_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(response.data, self.second_match)


class DeleteMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()
        self.post_both_matches()

    def test_delete_match(self):
        response = self.delete_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Match.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Match.objects.count(), 0)


class PermissionsTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()
        self.post_both_matches()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        updated_match = self.first_match.copy()
        updated_match['first_name'] = 'changed_first_name'

        response = self.client.post(self.base_url, self.first_match)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.first_model.pk), updated_match)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.first_model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
