from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Competition
from app.serializers import CompetitionSerializer


# ToDo add tests for /competition/<id>/matches/ endpoint

class CompetitionTestSetUp(APITestCase):
    first_model = Competition(pk=1, name='Name1', type='league')
    first_competition = CompetitionSerializer(first_model).data
    second_model = Competition(pk=2, name='Name2', type='tournament')
    second_competition = CompetitionSerializer(second_model).data
    url = reverse('competitions-list')

    def post_first_competition(self):
        self.client.post(self.url, self.first_competition, format='json')

    def post_both_competitions(self):
        self.client.post(self.url, self.first_competition, format='json')
        self.client.post(self.url, self.second_competition, format='json')


class CreateCompetitionTest(CompetitionTestSetUp):
    def test_create_competition(self):
        response = self.client.post(self.url, self.first_competition, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competition.objects.count(), 1)
        self.assertEqual(Competition.objects.get(pk=1), self.first_model)
        response = self.client.post(self.url, self.second_competition, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competition.objects.count(), 2)
        self.assertEqual(Competition.objects.get(pk=2), self.second_model)

    def test_not_create_competition_with_wrong_type(self):
        first_model = Competition(pk=1, name='Name1', type='WrongType')
        first_person = CompetitionSerializer(first_model).data
        response = self.client.post(self.url, first_person, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Competition.objects.count(), 0)


class ReadCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_both_competitions()

    def test_read_competition_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.first_competition)
        self.assertEqual(response.data[1], self.second_competition)

    def test_read_single_competition(self):
        response = self.client.get('/competitions/{}/'.format(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.first_competition)
        response = self.client.get('/competitions/{}/'.format(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_competition)


class UpdateCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.second_model = Competition(pk=1, name='Name2', type='tournament')
        self.second_competition = CompetitionSerializer(self.second_model).data
        self.post_first_competition()

    def test_update_competition(self):
        response = self.client.put('/competitions/{}/'.format(self.first_model.pk), self.second_competition)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_competition)
        response = self.client.get('/competitions/{}/'.format(self.first_model.pk))
        self.assertEqual(response.data, self.second_competition)


class DeleteCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_both_competitions()

    def test_delete_competition(self):
        response = self.client.delete('/competitions/{}/'.format(self.first_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Competition.objects.count(), 1)
        response = self.client.delete('/competitions/{}/'.format(self.second_model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Competition.objects.count(), 0)
