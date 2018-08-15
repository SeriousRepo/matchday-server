from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    RoleChoices = (('coach', 'coach'), ('player', 'player'), ('referee', 'referee'),)

    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=RoleChoices)
    birth_date = models.DateField(null=True)
    nationality = models.CharField(max_length=50, null=True)


class Player(models.Model):
    PositionChoices = (('goalkeeper', 'GK'), ('left-back', 'LB'),
                       ('centre-back', 'CB'), ('right-back', 'RB'),
                       ('left-midfield', 'LM'), ('centre-midfield', 'CM'),
                       ('right-midfield', 'RM'), ('centre-forward', 'CF'),)
    # ToDo fill more positions

    position = models.CharField(max_length=3, choices=PositionChoices)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)


class Competition(models.Model):
    TypeChoices = (('league', 'league'), ('tournament', 'tournament'),)

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TypeChoices)


class Match(models.Model):
    date = models.DateTimeField()
    main_referee = models.ForeignKey(Person, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=50)
    stadium = models.CharField(max_length=50)
    city = models.CharField(max_length=50)


class MatchTeam(models.Model):
    is_host = models.BooleanField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    coach = models.ForeignKey(Person, on_delete=models.CASCADE)


class EventInfo(models.Model):
    real_time = models.TimeField()
    match_minute = models.IntegerField()
    rank_points = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MatchEvent(models.Model):
    TypeChoices = (('first whistle', 'first whistle'), ('last whistle', 'last whistle'),
                   ('end of first half', 'end of first half'), ('begin of second half', 'begin of second half'),
                   ('end of second half', 'end of second half'), ('begin of extra time', 'begin of extra time'),
                   ('begin of extra time second half', 'begin of extra time second half'),
                   ('end of extra time first half', 'end of extra time first half'),
                   ('end of extra time second half', 'end of extra time second half'),
                   ('begin of penalty shoots', 'begin of penalty shoots'))

    description = models.CharField(max_length=50)
    event_type = models.CharField(max_length=100, choices=TypeChoices)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    event_info = models.OneToOneField(EventInfo, on_delete=models.CASCADE)


class TeamEvent(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match_team = models.ForeignKey(MatchTeam, on_delete=models.CASCADE)
    event_info = models.OneToOneField(EventInfo, on_delete=models.CASCADE)


class Goal(models.Model):
    description = models.CharField(max_length=50, null=True)
    team_event = models.OneToOneField(TeamEvent, on_delete=models.CASCADE)


class RedCard(models.Model):
    reason = models.CharField(max_length=50, null=True)
    team_event = models.OneToOneField(TeamEvent, on_delete=models.CASCADE)


class YellowCard(models.Model):
    reason = models.CharField(max_length=50, null=True)
    team_event = models.OneToOneField(TeamEvent, on_delete=models.CASCADE)


class Substitution(models.Model):
    reason = models.CharField(max_length=50, null=True)
    substituted_by = models.OneToOneField(Player, on_delete=models.CASCADE)
    team_event = models.OneToOneField(TeamEvent, on_delete=models.CASCADE)


class Assist(models.Model):
    description = models.CharField(max_length=50, null=True)
    assisted_to = models.OneToOneField(Player, on_delete=models.CASCADE)
    team_event = models.OneToOneField(TeamEvent, on_delete=models.CASCADE)
