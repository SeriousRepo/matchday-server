from app.serializers import *
from rest_framework.test import APIRequestFactory
from datetime import datetime, date, time


context = {'request': APIRequestFactory().get('/')}


class CompetitionRepresentation:
    def __init__(self, pk, type, year):
        self.model = Competition(pk=pk, name='name' + str(pk), type=type, area='Europe', year=year)
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
        self.model = Team(pk=pk, name='name' + str(pk), stadium='stadium' + str(pk), city=city, crest_url='some_crest')
        self.json = TeamSerializer(self.model).data


class TeamInMatchRepresentation:
    def __init__(self, pk, team, match, coach):
        self.model = TeamInMatch(pk=pk, is_host=False, team=team, match=match, coach=coach)
        self.json = TeamInMatchSerializer(self.model, context=context).data


class EventInfoRepresentation:
    def __init__(self, pk, user):
        self.model = EventInfo(pk=pk, real_time=time(18, 43), description='description'+str(pk),
                               match_minute=13, rank_points=137, user=user)
        self.json = EventInfoSerializer(self.model, context=context).data


class MatchEventRepresentation:
    def __init__(self, pk, match, event_info):
        self.model = MatchEvent(pk=pk, event_type='first whistle', match=match, event_info=event_info)
        self.json = MatchEventSerializer(self.model, context=context).data


class TeamEventRepresentation:
    def __init__(self, pk, player, participant, team_in_match, event_info, event_type='goal'):
        self.model = TeamEvent(pk=pk, event_type=event_type, player=player, event_participant=participant,
                               team_in_match=team_in_match, event_info=event_info)
        self.json = TeamEventSerializer(self.model, context=context).data
