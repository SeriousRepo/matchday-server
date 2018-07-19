from rest_framework import viewsets
from app.models import Team, Player, Match
from app.serializers import TeamSerializer, PlayerSerializer, MatchSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerPerTeamViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return Player.objects.filter(team=team_id)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class HomeMatchPerTeamViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return Match.objects.filter(home_team=team_id)


class AwayMatchPerTeamViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return Match.objects.filter(away_team=team_id)
