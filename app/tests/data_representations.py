from app.serializers import *
from rest_framework.test import APIRequestFactory
from datetime import datetime, date


context = {'request': APIRequestFactory().get('/')}


class CompetitionRepresentation:
    def __init__(self, pk, type):
        self.model = Competition(pk=pk, name='name' + str(pk), type=type)
        self.json = CompetitionSerializer(self.model).data


class MatchRepresentation:
    def __init__(self, pk, referee, competition):
        self.model = Match(pk=pk, date=datetime(2018, 11, 10, 20, 45),
                           main_referee=referee, competition=competition)
        self.json = MatchSerializer(self.model, context=context).data


class PersonRepresentation:
    def __init__(self, pk, role):
        self.model = Person(pk=pk, last_name='last_name' + str(pk), first_name='first_name' + str(pk),
                            role=role, birth_date=date(1961, 5, 13), nationality='nationality' + str(pk))
        self.json = PersonSerializer(self.model).data


class PlayerRepresentation:
    def __init__(self, pk, position, team, person):
        self.model = Player(pk=pk, position=position, team=team, person=person)
        self.json = PlayerSerializer(self.model, context=context).data


class TeamRepresentation:
    def __init__(self, pk, city='city'):
        self.model = Team(pk=pk, name='name' + str(pk), stadium='stadium' + str(pk), city=city)
        self.json = TeamSerializer(self.model).data


class MatchTeamRepresentation:
    def __init__(self, pk, is_host, team, match, coach):
        self.model = MatchTeam(pk=pk, is_host=is_host, team=team, match=match, coach=coach)
        self.json = MatchTeamSerializer(self.model, context=context).data
