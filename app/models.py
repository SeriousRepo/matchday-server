from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    RoleChoices = (('coach', 'coach'), ('player', 'player'), ('referee', 'referee'),)

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=RoleChoices)
    birth_date = models.DateField(null=True)
    nationality = models.CharField(max_length=50, null=True)


class Player(models.Model):
    PositionChoices = (('Goalkeeper', 'Goalkeeper'), ('Defender', 'Defender'),
                       ('Midfielder', 'Midfielder'), ('Attacker', 'Attacker'),)

    position = models.CharField(max_length=50, choices=PositionChoices, null=True)
    shirt_number = models.IntegerField(null=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='players')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Competition(models.Model):
    TypeChoices = (('league', 'league'), ('tournament', 'tournament'),)

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TypeChoices)
    area = models.CharField(max_length=50)
    year = models.IntegerField()


class Match(models.Model):
    DurationChoices = (('regular', 'regular'), ('extra_time', 'extra_time'), ('penalty_shootout', 'penalty_shootout'))
    StatusChoices = (('in_play', 'in_play'), ('scheduled', 'scheduled'), ('finished', 'finished'))

    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    main_referee = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_query_name='match')
    duration = models.CharField(max_length=50, choices=DurationChoices, null=True)
    stage = models.CharField(max_length=50, null=True)
    group = models.CharField(max_length=50)
    matchday = models.IntegerField()
    status = models.CharField(max_length=50)


class Team(models.Model):
    name = models.CharField(max_length=50)
    stadium = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    crest_url = models.CharField(max_length=200, null=True)


class TeamInMatch(models.Model):
    is_host = models.BooleanField()
    goals = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_query_name='team_in_match')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='teams', related_query_name='team_in_match')
    coach = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)


class EventInfo(models.Model):
    real_time = models.TimeField()
    match_minute = models.IntegerField()
    description = models.CharField(max_length=50, null=True)
    rank_points = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MatchEvent(models.Model):
    TypeChoices = (('first whistle', 'first whistle'), ('last whistle', 'last whistle'),
                   ('end of first half', 'end of first half'), ('begin of second half', 'begin of second half'),
                   ('end of second half', 'end of second half'), ('begin of extra time', 'begin of extra time'),
                   ('begin of extra time second half', 'begin of extra time second half'),
                   ('end of extra time first half', 'end of extra time first half'),
                   ('end of extra time second half', 'end of extra time second half'),
                   ('begin of penalty shoots', 'begin of penalty shoots'))

    event_type = models.CharField(max_length=100, choices=TypeChoices)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    event_info = models.OneToOneField(EventInfo, on_delete=models.CASCADE)


class TeamEvent(models.Model):
    TypeChoices = (('yellow_card', 'yellow_card'), ('red_card', 'red_card'),
                   ('goal', 'goal'), ('substitution', 'substitution'))
    event_type = models.CharField(max_length=20, choices=TypeChoices)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event_participant = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='participant')
    team_in_match = models.ForeignKey(TeamInMatch, on_delete=models.CASCADE)
    event_info = models.OneToOneField(EventInfo, on_delete=models.CASCADE)
