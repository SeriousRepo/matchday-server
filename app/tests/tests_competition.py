from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
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
        self.register_user()
        self.client.post(self.url, self.first_competition, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)

    def post_both_competitions(self):
        self.register_user()
        self.client.post(self.url, self.first_competition, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.post(self.url, self.second_competition, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)

    def register_user(self):
        url = reverse('account-create')
        user = {
            'username': 'username',
            'email': 'email1@email.email',
            'password': 'password',
        }
        self.client.post(url, user, format='json')
        user = User.objects.get(username='username')
        self.token = Token.objects.get(user=user)


class CreateCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.register_user()

    def test_create_competition(self):
        response = self.client.post(self.url, self.first_competition, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competition.objects.count(), 1)
        self.assertEqual(Competition.objects.get(pk=1), self.first_model)
        response = self.client.post(self.url, self.second_competition, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competition.objects.count(), 2)
        self.assertEqual(Competition.objects.get(pk=2), self.second_model)

    def test_not_create_competition_with_wrong_type(self):
        first_model = Competition(pk=1, name='Name1', type='WrongType')
        first_person = CompetitionSerializer(first_model).data
        response = self.client.post(self.url, first_person, format='json', HTTP_AUTHORIZATION='Token ' + self.token.key)
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
        response = self.client.put('/competitions/{}/'.format(self.first_model.pk), self.second_competition, HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.second_competition)
        response = self.client.get('/competitions/{}/'.format(self.first_model.pk))
        self.assertEqual(response.data, self.second_competition)


class DeleteCompetitionTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_both_competitions()

    def test_delete_competition(self):
        response = self.client.delete('/competitions/{}/'.format(self.first_model.pk), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Competition.objects.count(), 1)
        response = self.client.delete('/competitions/{}/'.format(self.second_model.pk), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Competition.objects.count(), 0)


class PermissionsTest(CompetitionTestSetUp):
    def setUp(self):
        self.post_both_competitions()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get('{}{}/'.format(self.url, self.first_model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        updated_competition = self.first_competition.copy()
        updated_competition['name'] = 'changed_name'

        response = self.client.post(self.url, self.first_competition)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put('{}{}/'.format(self.url, self.first_model.pk), updated_competition)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete('{}{}/'.format(self.url, self.first_model.pk))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
