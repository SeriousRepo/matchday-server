from rest_framework import serializers
from app.models import User, Person, Player, Match, Competition


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'join_date', 'rank_points')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'last_name', 'first_name', 'role', 'birth_date')


class PlayerSerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=True)

    class Meta:
        model = Player
        fields = ('id', 'position', 'person')

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        person = PersonSerializer.create(PersonSerializer(), validated_data=person_data)
        player, created = Player.objects.update_or_create(position=validated_data.pop('position'), person=person)
        return player


class MatchSerializer(serializers.ModelSerializer):
    main_referee = PersonSerializer(required=True)

    class Meta:
        model = Match
        fields = ('id', 'date', 'main_referee', 'competition')

    def create(self, validated_data):
        main_referee_data = validated_data.pop('main_referee')
        main_referee = PersonSerializer.create(PersonSerializer(), validated_data=main_referee_data)
        match, created = Match.objects.update_or_create(date=validated_data.pop('date'),
                                                        main_referee=main_referee,
                                                        competition=validated_data.pop('competition'))
        return match


class CompetitionSerializer(serializers.ModelSerializer):
    matches = serializers.HyperlinkedRelatedField(many=True,
                                                  read_only=True,
                                                  view_name='match-detail')

    class Meta:
        model = Competition
        fields = ('id', 'name', 'type', 'matches')
