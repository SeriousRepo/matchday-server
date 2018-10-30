from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
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
        fields = ('id', 'name', 'role', 'birth_date', 'nationality')
        validators = [
            UniqueTogetherValidator(
                queryset=Person.objects.all(),
                fields=('name', 'birth_date')
            )
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'stadium', 'city', 'crest_url')
        validators = [
            UniqueTogetherValidator(
                queryset=Team.objects.all(),
                fields=('name', 'stadium')
            )
        ]


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    person = serializers.HyperlinkedRelatedField(queryset=Person.objects.filter(role='player'), view_name='people-detail')
    team = serializers.HyperlinkedRelatedField(queryset=Team.objects.all(), view_name='teams-detail')

    class Meta:
        model = Player
        fields = ('id', 'position', 'shirt_number', 'team', 'person')


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    main_referee = serializers.HyperlinkedRelatedField(queryset=Person.objects.filter(role='referee'), view_name='people-detail')
    competition = serializers.HyperlinkedRelatedField(queryset=Competition.objects.all(), view_name='competitions-detail')

    class Meta:
        model = Match
        fields = ('id', 'date', 'main_referee', 'competition')


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'name', 'type', 'area', 'year')
        validators = [
            UniqueTogetherValidator(
                queryset=Competition.objects.all(),
                fields=('name', 'year')
            )
        ]


class TeamInMatchSerializer(serializers.HyperlinkedModelSerializer):
    # ToDo add restriction to different teams in single match
    team = serializers.HyperlinkedRelatedField(queryset=Team.objects.all(), view_name='teams-detail')
    match = serializers.HyperlinkedRelatedField(queryset=Match.objects.all(), view_name='matches-detail')
    coach = serializers.HyperlinkedRelatedField(queryset=Person.objects.filter(role='coach'), view_name='people-detail')

    class Meta:
        model = TeamInMatch
        fields = ('id', 'is_host', 'team', 'match', 'coach')


class EventInfoSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='users-detail')

    class Meta:
        model = EventInfo
        fields = ('id', 'real_time', 'match_minute', 'description', 'rank_points', 'user')


class MatchEventSerializer(serializers.ModelSerializer):
    match = serializers.HyperlinkedRelatedField(queryset=Match.objects.all(), view_name='matches-detail')
    event_info = EventInfoSerializer(required=True)

    class Meta:
        model = MatchEvent
        fields = ('id', 'event_type', 'match', 'event_info')

    def create(self, validated_data):
        event_data = validated_data.pop('event_info')
        event = EventInfoSerializer.create(EventInfoSerializer(), validated_data=event_data)
        match_event, created = MatchEvent.objects.update_or_create(event_type=validated_data.pop('event_type'),
                                                                   match=validated_data.pop('match'),
                                                                   event_info=event)
        return match_event


class TeamEventSerializer(serializers.HyperlinkedModelSerializer):
    player = serializers.HyperlinkedRelatedField(queryset=Player.objects.all(), view_name='players-detail')
    event_participant = serializers.HyperlinkedRelatedField(queryset=Player.objects.all(), view_name='players-detail')
    team_in_match = serializers.HyperlinkedRelatedField(queryset=TeamInMatch.objects.all(), view_name='team_in_matchs-detail')
    event_info = EventInfoSerializer(required=True)

    class Meta:
        model = TeamEvent
        fields = ('id', 'event_type', 'player', 'event_participant', 'team_in_match', 'event_info')

    def create(self, validated_data):
        event_data = validated_data.pop('event_info')
        event = EventInfoSerializer.create(EventInfoSerializer(), validated_data=event_data)
        team_event, created = TeamEvent.objects.update_or_create(event_type=validated_data.pop('event_type'),
                                                                 player=validated_data.pop('player'),
                                                                 event_participant=validated_data.pop('event_participant'),
                                                                 team_in_match=validated_data.pop('team_in_match'),
                                                                 event_info=event)
        return team_event

    def update(self, instance, validated_data):
        validated_event_info = validated_data.get('event_info', instance.event_info)
        event_info = EventInfoSerializer.update(EventInfoSerializer(), instance.event_info, validated_data=validated_event_info)
        instance.event_type = validated_data.get('event_type', instance.event_type)
        instance.player = validated_data.get('player', instance.player)
        instance.event_participant = validated_data.get('event_participant', instance.event_participant)
        instance.team_in_match = validated_data.get('team_in_match', instance.team_in_match)
        instance.event_info = event_info
        instance.save()
        return instance
