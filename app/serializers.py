from rest_framework import serializers
from app.models import User, Person, Player, Match, Competition, Team, MatchTeam


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'join_date', 'rank_points')


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
        player, created = Player.objects.update_or_create(position=validated_data.pop('position'), person=person, team=validated_data.pop('team'))
        return player


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    # ToDo restrict that user can post only referee person
    main_referee = serializers.HyperlinkedRelatedField(queryset=Person.objects.all(), view_name='people-detail')
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
        fields = ('id', 'name', 'points', 'goals_scored', 'goals_conceded')


class MatchTeamSerializer(serializers.ModelSerializer):
    # ToDo hyperlinked
    # ToDo add restriction to different teams in single match
    class Meta:
        model = MatchTeam
        fields = ('id', 'goals_amount', 'is_host', 'team', 'match', 'coach')
