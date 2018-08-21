from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils import timezone
from app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined')


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            max_length=100,
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(required=True, min_length=8, write_only=True)
    date_joined = serializers.DateTimeField(default=timezone.now)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'date_joined')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'last_name', 'first_name', 'role', 'birth_date', 'nationality')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'stadium', 'city')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    person = PersonSerializer(required=True)
    team = serializers.HyperlinkedRelatedField(queryset=Team.objects.all(), view_name='teams-detail')

    class Meta:
        model = Player
        fields = ('id', 'position', 'team', 'person')

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        person_data['role'] = 'player'
        person = PersonSerializer.create(PersonSerializer(), validated_data=person_data)
        player, created = Player.objects.update_or_create(position=validated_data.pop('position'),
                                                          person=person,
                                                          team=validated_data.pop('team'))
        return player


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    # ToDo restrict that user can post only referee person
    main_referee = serializers.HyperlinkedRelatedField(queryset=Person.objects.filter(role='referee'), view_name='people-detail')
    competition = serializers.HyperlinkedRelatedField(queryset=Competition.objects.all(), view_name='competitions-detail')

    class Meta:
        model = Match
        fields = ('id', 'date', 'main_referee', 'competition')


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'name', 'type')


class MatchTeamSerializer(serializers.HyperlinkedModelSerializer):
    # ToDo add restriction to different teams in single match
    team = serializers.HyperlinkedRelatedField(queryset=Team.objects.all(), view_name='teams-detail')
    match = serializers.HyperlinkedRelatedField(queryset=Match.objects.all(), view_name='matches-detail')
    coach = serializers.HyperlinkedRelatedField(queryset=Person.objects.filter(role='coach'), view_name='people-detail')

    class Meta:
        model = MatchTeam
        fields = ('id', 'is_host', 'team', 'match', 'coach')


class EventInfoSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='users-detail')

    class Meta:
        model = EventInfo
        fields = ('id', 'real_time', 'match_minute', 'rank_points', 'user')


class MatchEventSerializer(serializers.ModelSerializer):
    match = serializers.HyperlinkedRelatedField(queryset=Match.objects.all(), view_name='matches-detail')
    event_info = EventInfoSerializer(required=True)

    class Meta:
        model = MatchEvent
        fields = ('id', 'description', 'event_type', 'match', 'event_info')

    def create(self, validated_data):
        event_data = validated_data.pop('event_info')
        event = EventInfoSerializer.create(EventInfoSerializer(), validated_data=event_data)
        match_event, created = MatchEvent.objects.update_or_create(description=validated_data.pop('description'),
                                                                   match=validated_data.pop('match'),
                                                                   event_info=event)
        return match_event


class TeamEventSerializer(serializers.HyperlinkedModelSerializer):
    player = serializers.HyperlinkedRelatedField(queryset=Player.objects.all(), view_name='players-detail')
    match_team = serializers.HyperlinkedRelatedField(queryset=MatchTeam.objects.all(), view_name='match_teams-detail')
    event_info = EventInfoSerializer(required=True)

    class Meta:
        model = TeamEvent
        fields = ('id', 'player', 'match_team', 'event_info')

    def create(self, validated_data):
        event_data = validated_data.pop('event_info')
        event = EventInfoSerializer.create(EventInfoSerializer(), validated_data=event_data)
        # ToDo check if player
        team_event, created = TeamEvent.objects.update_or_create(player=validated_data.pop('player'),
                                                                 match_team=validated_data.pop('match_team'),
                                                                 event_info=event)
        return team_event


class GoalSerializer(serializers.ModelSerializer):
    team_event = TeamEventSerializer(required=True)

    class Meta:
        model = Goal
        fields = ('id', 'description', 'team_event')

    def create(self, validated_data):
        event_data = validated_data.pop('team_event')
        event = TeamEventSerializer.create(TeamEventSerializer(), validated_data=event_data)
        goal, created = Goal.objects.all().update_or_create(description=validated_data.pop('description'),
                                                            team_event=event)
        return goal


class RedCardSerializer(serializers.ModelSerializer):
    team_event = TeamEventSerializer(required=True)

    class Meta:
        model = RedCard
        fields = ('id', 'reason', 'team_event')

    def create(self, validated_data):
        event_data = validated_data.pop('team_event')
        event = TeamEventSerializer.create(TeamEventSerializer(), validated_data=event_data)
        red_card, created = RedCard.objects.all().update_or_create(reason=validated_data.pop('reason'),
                                                                   team_event=event)
        return red_card


class YellowCardSerializer(serializers.ModelSerializer):
    team_event = TeamEventSerializer(required=True)

    class Meta:
        model = YellowCard
        fields = ('id', 'reason', 'team_event')

    def create(self, validated_data):
        event_data = validated_data.pop('team_event')
        event = TeamEventSerializer.create(TeamEventSerializer(), validated_data=event_data)
        yellow_card, created = YellowCard.objects.all().update_or_create(reason=validated_data.pop('reason'),
                                                                         team_event=event)
        return yellow_card


class SubstitutionSerializer(serializers.HyperlinkedModelSerializer):
    team_event = TeamEventSerializer(required=True)
    # ToDo check if not the same player
    substituted_by = serializers.HyperlinkedRelatedField(queryset=Player.objects.all(), view_name='players-detail')

    class Meta:
        model = Substitution
        fields = ('id', 'reason', 'substituted_by', 'team_event')

    def create(self, validated_data):
        event_data = validated_data.pop('team_event')
        event = TeamEventSerializer.create(TeamEventSerializer(), validated_data=event_data)
        substitution, created = Substitution.objects.all().update_or_create(reason=validated_data.pop('reason'),
                                                                            substituted_by=validated_data.pop('substituted_by'),
                                                                            team_event=event)
        return substitution


class AssistSerializer(serializers.HyperlinkedModelSerializer):
    team_event = TeamEventSerializer(required=True)
    # ToDo check if not the same player
    assisted_to = serializers.HyperlinkedRelatedField(queryset=Player.objects.all(), view_name='players-detail')

    class Meta:
        model = Assist
        fields = ('id', 'description', 'assisted_to', 'team_event')

    def create(self, validated_data):
        event_data = validated_data.pop('team_event')
        event = TeamEventSerializer.create(TeamEventSerializer(), validated_data=event_data)
        assist, created = Assist.objects.all().update_or_create(description=validated_data.pop('description'),
                                                                assisted_to=validated_data.pop('assisted_to'),
                                                                team_event=event)
        return assist
