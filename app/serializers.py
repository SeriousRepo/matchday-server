from rest_framework import serializers
from app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'join_date')


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
        person = PersonSerializer.create(PersonSerializer(), validated_data=person_data)
        # ToDo check if player
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
    event = EventInfoSerializer(required=True)

    class Meta:
        model = MatchEvent
        fields = ('id', 'description', 'match', 'event')

    def create(self, validated_data):
        event_data = validated_data.pop('event')
        event = EventInfoSerializer.create(EventInfoSerializer(), validated_data=event_data)
        match_event, created = MatchEvent.objects.update_or_create(description=validated_data.pop('description'),
                                                                   match=validated_data.pop('match'),
                                                                   event=event)
        return match_event


class TeamEventSerializer(serializers.HyperlinkedModelSerializer):
    player = serializers.HyperlinkedRelatedField(queryset=Player.objects.all(), view_name='players-detail')
    match_team = serializers.HyperlinkedRelatedField(queryset=MatchTeam.objects.all(), view_name='match-team-detail')
    event = EventInfoSerializer(required=True)

    class Meta:
        model = TeamEvent
        fields = ('id', 'event_type', 'player', 'match_team', 'event')

    def create(self, validated_data):
        event_data = validated_data.pop('event')
        event = EventInfoSerializer.create(EventInfoSerializer(), validated_data=event_data)
        # ToDo check if player
        match_event, created = MatchEvent.objects.update_or_create(event_type=validated_data.pop('event_type'),
                                                                   player=validated_data.pop('player'),
                                                                   match_team=validated_data.pop('match_team'),
                                                                   event=event)
        return match_event


#class
