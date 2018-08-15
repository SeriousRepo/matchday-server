from rest_framework import status, viewsets, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers import *


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(APIView):
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


class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid()
        user = User.objects.get(email=serializer.validated_data['email'])
        token = Token.objects.get(user=user)
        response_data = {
            'email': user.email,
            'token': token.key
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PeopleViewSet(viewsets.ModelViewSet):
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
