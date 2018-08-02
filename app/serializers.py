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


class PlayerSerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=True)

    class Meta:
        model = Player
        fields = ('id', 'position', 'person', 'team')

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        person = PersonSerializer.create(PersonSerializer(), validated_data=person_data)
        # ToDo check if player
        player, created = Player.objects.update_or_create(position=validated_data.pop('position'), person=person, team=validated_data.pop('team'))
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


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'stadium', 'city')


class MatchTeamSerializer(serializers.HyperlinkedModelSerializer):
    # ToDo add restriction to different teams in single match
    team = serializers.HyperlinkedRelatedField(queryset=Team.objects.all(), view_name='teams-detail')
    match = serializers.HyperlinkedRelatedField(queryset=Match.objects.all(), view_name='matches-detail')
    coach = serializers.HyperlinkedRelatedField(queryset=Person.objects.filter(role='coach'), view_name='people-detail')

    class Meta:
        model = MatchTeam
        fields = ('id', 'is_host', 'team', 'match', 'coach')


class EventInfoSerializer(serializers.HyperlinkedRelatedField):
    user = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='users-detail')

    class Meta:
        model = EventInfo
        fields = ('id', 'real_time', 'match_minute', 'rank_points', 'user')
