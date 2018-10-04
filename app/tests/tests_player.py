from rest_framework.reverse import reverse
from rest_framework import status
from app.models import Player
from app.tests.helpers.tests_setup_base import TestsSetUpBase
from app.tests.helpers.common_data import player, team


class PlayerTestSetUp(TestsSetUpBase):
    base_url = reverse('players-list')
    player1 = player(1)
    player2 = player(2)

    def post_nested(self):
        self.register_user()
        self.post_method(reverse('teams-list'), team(1).json)
        self.post_method(reverse('teams-list'), team(2).json)

    def post_single_player(self):
        self.post_nested()
        self.post_method(self.base_url, self.player1.json)

    def post_two_players(self):
        self.post_nested()
        self.post_method(self.base_url, self.player1.json)
        self.post_method(self.base_url, self.player2.json)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)


class CreatePlayerTest(PlayerTestSetUp):
    def setUp(self):
        self.post_nested()

    def test_create_player(self):
        response = self.post_method(self.base_url, self.player1.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(response.data, self.player1.json)
        response = self.post_method(self.base_url, self.player2.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 2)
        self.assertEqual(response.data, self.player2.json)

    # Todo restrict adding same player several times and uncomment
    #def test_restrict_creating_same_player_several_times(self):
    #    self.post_method(self.base_url, self.player1.json)
    #    response = self.post_method(self.base_url, self.player1.json)
    #    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
# Todo watch player serializer and uncomment
#class WrongCreationOfPlayerTest(PlayerTestSetUp):
#    def setUp(self):
#        self.post_nested()

#    def test_not_create_player_when_non_player_person_type(self):
#        referee = PersonRepresentation(1, 'referee')
#        non_player_type_person = PlayerRepresentation(1, 'CB', self.team.model, referee.model)
#        response = self.post_method(self.base_url, non_player_type_person.json)
#        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


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


# Todo resolve problem with nested serializer, and uncomment

#class UpdatePlayerTest(PlayerTestSetUp):
#    def setUp(self):
#        self.post_single_player()
#        self.updated_player = PlayerRepresentation(1, 'GK', self.team.model, self.person2.model)

#    def test_update_player(self):
#        response = self.put_method(self.get_nth_element_url(self.player1.model.pk), self.updated_player.json)
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertEqual(response.data, self.updated_player.json)
#        response = self.get_method(self.get_nth_element_url(self.player1.model.pk))
#        self.assertEqual(response.data, self.updated_player.json)


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

        #Todo uncomment after above problem resolution
        #response = self.client.put(self.get_nth_element_url(self.player1.model.pk), updated_player_json, format='json')
        #self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        response = self.client.delete(self.get_nth_element_url(self.player1.model.pk), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
