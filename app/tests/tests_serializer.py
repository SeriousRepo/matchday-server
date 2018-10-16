from app.serializers import *
from rest_framework.test import APITestCase, APIRequestFactory


"""class TestSerializer(APITestCase):
    def test(self):
        team = Team(pk=1, name='name')
        person = Person(pk=1, last_name='last_name', first_name='first_name', role='player')
        player = Player(pk=1, person=person, team=team, position='GK')
        player2 = Player(pk=2, person=person, team=team, position='GK')
        serializer = PlayerSerializer(player, context={'request': APIRequestFactory().get('/')})
        serializer2 = PlayerSerializer(player2, context={'request': APIRequestFactory().get('/')})
        print(serializer.data)
        print(serializer2.data)

    #def test2(self):
    #    TeamEventSerializer
"""
