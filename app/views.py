from rest_framework import viewsets
from app.serializers import *


"""class UsersViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
"""

class PersonsViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class RefereesViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(role='referee')
    serializer_class = PersonSerializer


class CoachesViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(role='coach')
    serializer_class = PersonSerializer


class RefereesPerCompetitionViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer

    def get_queryset(self):
        competition_id = self.kwargs['competition_id']
        return Person.objects.filter(match__competition=competition_id)


class PlayersViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class MatchesViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchesPerCompetitionViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer

    def get_queryset(self):
        competition_id = self.kwargs['competition_id']
        return Match.objects.filter(competition=competition_id)


class CompetitionsViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchTeamsViewSet(viewsets.ModelViewSet):
    queryset = MatchTeam.objects.all()
    serializer_class = MatchTeamSerializer


class EventInfosViewSet(viewsets.ModelViewSet):
    queryset = EventInfo.objects.all()
    serializer_class = EventInfoSerializer


class MatchEventsViewSet(viewsets.ModelViewSet):
    queryset = MatchEvent.objects.all()
    serializer_class = MatchEventSerializer


class TeamEventsViewSet(viewsets.ModelViewSet):
    queryset = TeamEvent.objects.all()
    serializer_class = TeamEventSerializer


class GoalsViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class RedCardsViewSet(viewsets.ModelViewSet):
    queryset = RedCard.objects.all()
    serializer_class = RedCardSerializer


class YellowCardsViewSet(viewsets.ModelViewSet):
    queryset = YellowCard.objects.all()
    serializer_class = YellowCardSerializer


class SubstitutionsViewSet(viewsets.ModelViewSet):
    queryset = Substitution.objects.all()
    serializer_class = SubstitutionSerializer


class AssistsViewSet(viewsets.ModelViewSet):
    queryset = Assist.objects.all()
    serializer_class = AssistSerializer
