from rest_framework import serializers
from app.models import Team, Player


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'points', 'goals_scored', 'goals_conceded')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'last_name', 'first_name', 'birth_date')
