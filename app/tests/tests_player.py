from rest_framework.reverse import reverse
from rest_framework import status
from app.models import Player
from app.tests.helpers.tests_setup_base import TestsSetUpBase
from app.tests.helpers.common_data import player, team, player_person, referee_person
from app.tests.helpers.data_representations import PlayerRepresentation


class PlayerTestSetUp(TestsSetUpBase):
    base_url = reverse('players-list')
    player1 = player(1)
    player2 = player(2)
    updated_player = PlayerRepresentation(1, team(1).model, player_person(2).model)

    def post_nested_to_single(self, person=player_person(1)):
        self.register_user()
        self.post_method(reverse('people-list'), person.json)
        self.post_method(reverse('teams-list'), team(1).json)

    def post_nested_to_both(self):
        self.post_nested_to_single()
        self.post_method(reverse('people-list'), player_person(2).json)

    def post_single_player(self):
        self.post_nested_to_single()
        self.post_method(self.base_url, self.player1.json)

    def post_two_players(self):
        self.post_nested_to_both()
        self.post_method(self.base_url, self.player1.json)
        self.post_method(self.base_url, self.player2.json)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)


class CreatePlayersWithDifferentPeopleTest(PlayerTestSetUp):
    def test_create_players_to_different_people(self):
        self.post_nested_to_both()
        response = self.post_method(self.base_url, self.player1.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(response.data, self.player1.json)
        response = self.post_method(self.base_url, self.player2.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 2)
        self.assertEqual(response.data, self.player2.json)


class CreatePlayersWithTheSamePersonTest(PlayerTestSetUp):
    def test_create_players_to_the_same_person(self):
        self.post_nested_to_single()
        player2_with_the_same_person = PlayerRepresentation(2, team(1).model, player_person(1).model)
        response = self.post_method(self.base_url, self.player1.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(response.data, self.player1.json)
        response = self.post_method(self.base_url, player2_with_the_same_person.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 2)
        self.assertEqual(response.data, player2_with_the_same_person.json)


class WrongCreationOfPlayerTest(PlayerTestSetUp):
    def test_not_create_player_when_non_player_person_type(self):
        referee = referee_person(1)
        self.post_nested_to_single(referee)
        non_player_type_person = PlayerRepresentation(1, team(1).model, referee.model)
        response = self.post_method(self.base_url, non_player_type_person.json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class ReadPlayerTest(PlayerTestSetUp):
    def setUp(self):
        self.post_two_players()

    def test_read_player_list(self):
        response = self.get_method(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.player1.json)
        self.assertEqual(response.data[1], self.player2.json)

    def test_read_single_player(self):
        response = self.get_method(self.get_nth_element_url(self.player1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.player1.json)
        response = self.get_method(self.get_nth_element_url(self.player2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.player2.json)


class UpdatePlayerTest(PlayerTestSetUp):
    def setUp(self):
        self.post_two_players()

    def test_update_player(self):
        response = self.put_method(self.get_nth_element_url(self.player1.model.pk), self.updated_player.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.updated_player.json)
        response = self.get_method(self.get_nth_element_url(self.player1.model.pk))
        self.assertEqual(response.data, self.updated_player.json)


class DeletePlayerTest(PlayerTestSetUp):
    def setUp(self):
        self.post_two_players()

    def test_delete_player(self):
        response = self.delete_method(self.get_nth_element_url(self.player1.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Player.objects.count(), 1)
        response = self.delete_method(self.get_nth_element_url(self.player2.model.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Player.objects.count(), 0)


class PermissionsTest(PlayerTestSetUp):
    def setUp(self):
        self.post_two_players()

    def test_allow_safe_http_methods_without_authorization(self):
        response = self.get_method(self.base_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.get_method(self.get_nth_element_url(self.player1.model.pk))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_restrict_non_safe_http_methods_without_authorization(self):
        response = self.client.post(self.base_url, self.player1.json, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.put(self.get_nth_element_url(self.player1.model.pk), self.updated_player.json, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.player1.model.pk), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
