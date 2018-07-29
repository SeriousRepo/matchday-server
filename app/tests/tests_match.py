from rest_framework.reverse import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Match, Person, Competition
from app.serializers import MatchSerializer, PersonSerializer, CompetitionSerializer
from datetime import date, datetime


# ToDo add more referees and competitions

class MatchTestSetUp(APITestCase):
    url = reverse('matches-list')

    def post_nested(self):
        self.first_referee_model = Person(pk=1, last_name='LastName1', first_name='FirstName1',
                                          role='coach', birth_date=date(1961, 5, 13))
        self.first_referee = PersonSerializer(self.first_referee_model).data
        self.first_competition_model = Competition(pk=1, name='Name1', type='league')
        self.first_competition = CompetitionSerializer(self.first_competition_model).data
        self.client.post(reverse('people-list'), self.first_referee, format='json')
        self.client.post(reverse('competitions-list'), self.first_competition, format='json')

    def post_first_match(self):
        self.set_first_match()
        self.client.post(self.url, self.first_match, format='json')

    def set_first_match(self):
        self.first_model = Match(pk=1, date=datetime(2018, 11, 10, 20, 45),
                                 main_referee=self.first_referee_model, competition=self.first_competition_model)
        self.first_match = MatchSerializer(self.first_model).data
        self.first_match.main_referee = reverse_lazy('api-root', request=self.client.get('/people/{}/'.format(self.first_model.main_referee.pk)))

    def set_second_match(self):
        self.second_model = Match(pk=2, date=datetime(2019, 1, 3, 20, 45),
                                  main_referee=self.first_referee_model, competition=self.first_competition_model)
        self.second_match = MatchSerializer(self.second_model).data

    def post_both_matches(self):
        self.set_first_match()
        self.set_second_match()
        self.client.post(self.url, self.first_match, format='json')
        self.client.post(self.url, self.second_match, format='json')


class CreateMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()
        self.set_first_match()
        self.set_second_match()

    def test_create_match(self):
        response = self.client.post(self.url, self.first_match, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(response.data, self.first_match)
        response = self.client.post(self.url, self.second_match, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 2)
        self.assertEqual(response.data, self.second_match)


class ReadMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()
        self.post_both_matches()

    def test_read_match_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.first_match)
        self.assertEqual(response.data[1], self.second_match)

    def test_read_single_match(self):
        response = self.client.get('/matches/{}/'.format(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.first_match)
        response = self.client.get('/matches/{}/'.format(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_match)


class UpdateMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()
        self.second_model = Match(pk=1, date=datetime(2019, 1, 3, 20, 45),
                                  main_referee=self.first_referee_model, competition=self.first_competition_model)
        self.second_match = MatchSerializer(self.second_model).data
        self.post_first_match()

    def test_update_match(self):
        response = self.client.put('/matches/{}/'.format(self.first_model.pk), self.second_match)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_match)
        response = self.client.get('/matches/{}/'.format(self.first_model.pk))
        self.assertEqual(response.data, self.second_match)


class DeleteMatchTest(MatchTestSetUp):
    def setUp(self):
        self.post_nested()
        self.post_both_matches()

    def test_delete_match(self):
        response = self.client.delete('/matches/{}/'.format(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Match.objects.count(), 1)
        response = self.client.delete('/matches/{}/'.format(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Match.objects.count(), 0)
