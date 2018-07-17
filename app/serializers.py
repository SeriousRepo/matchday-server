from rest_framework import serializers
from app.models import Team, Player


class TeamSerializer(serializers.ModelSerializer):
    players = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='player-detail'
    )

    class Meta:
        model = Team
        fields = ('id', 'name', 'points', 'goals_scored', 'goals_conceded', 'players')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'last_name', 'first_name', 'birth_date', 'team')
