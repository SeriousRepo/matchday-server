from rest_framework import serializers
from app.models import Team, Player, Match


class TeamSerializer(serializers.ModelSerializer):
    players = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='player-detail'
    )

    home_matches = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='match-detail'
    )

    away_matches = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='match-detail'
    )

    class Meta:
        model = Team
        fields = ('id', 'name', 'points', 'goals_scored', 'goals_conceded', 'players', 'home_matches', 'away_matches')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'last_name', 'first_name', 'birth_date', 'team')


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'date', 'home_goals', 'away_goals', 'home_team', 'away_team')
