from app.serializers import *
from rest_framework.test import APIRequestFactory
from datetime import datetime, date, time


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
    def __init__(self, pk, team, person):
        self.model = Player(pk=pk, position='GK', team=team, person=person)
        self.json = PlayerSerializer(self.model, context=context).data


class TeamRepresentation:
    def __init__(self, pk, city='city'):
        self.model = Team(pk=pk, name='name' + str(pk), stadium='stadium' + str(pk), city=city)
        self.json = TeamSerializer(self.model).data


class MatchTeamRepresentation:
    def __init__(self, pk, team, match, coach):
        self.model = MatchTeam(pk=pk, is_host=True, team=team, match=match, coach=coach)
        self.json = MatchTeamSerializer(self.model, context=context).data


class EventInfoRepresentation:
    def __init__(self, pk, user):
        self.model = EventInfo(pk=pk, real_time=time(18, 43), match_minute=13, rank_points=137, user=user)
        self.json = EventInfoSerializer(self.model, context=context).data


class MatchEventRepresentation:
    def __init__(self, pk, match, event_info):
        self.model = MatchEvent(pk=pk, description='description'+str(pk),
                                event_type='first whistle', match=match, event_info=event_info)
        self.json = MatchEventSerializer(self.model, context=context).data
