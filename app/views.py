from rest_framework import viewsets
from app.models import User, Person, Player, Match, Competition, Team, MatchTeam
from app.serializers import UserSerializer, PersonSerializer, PlayerSerializer,\
                            MatchSerializer, CompetitionSerializer, TeamSerializer,\
                            MatchTeamSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchTeamViewSet(viewsets.ModelViewSet):
    queryset = MatchTeam.objects.all()
    serializer_class = MatchTeamSerializer
