from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers import *


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PeopleViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class RefereesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.filter(role='referee')
    serializer_class = PersonSerializer


class CoachesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.filter(role='coach')
    serializer_class = PersonSerializer


class RefereesPerCompetitionViewSet(viewsets.ReadOnlyModelViewSet):
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


class MatchesPerCompetitionViewSet(viewsets.ReadOnlyModelViewSet):
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


class TeamInMatchsViewSet(viewsets.ModelViewSet):
    queryset = TeamInMatch.objects.all()
    serializer_class = TeamInMatchSerializer


class EventInfosViewSet(viewsets.ModelViewSet):
    queryset = EventInfo.objects.all()
    serializer_class = EventInfoSerializer


class MatchEventsViewSet(viewsets.ModelViewSet):
    queryset = MatchEvent.objects.all()
    serializer_class = MatchEventSerializer


class TeamEventsViewSet(viewsets.ModelViewSet):
    queryset = TeamEvent.objects.all()
    serializer_class = TeamEventSerializer
