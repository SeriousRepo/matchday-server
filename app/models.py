from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    RoleChoices = (('coach', 'coach'), ('player', 'player'), ('referee', 'referee'),)

    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, null=True)
    role = models.CharField(max_length=10, choices=RoleChoices)
    birth_date = models.DateField(null=True)
    nationality = models.CharField(max_length=50, null=True)


class Player(models.Model):
    PositionChoices = (('GK', 'goalkeeper'), ('LB', 'left-back'),
                       ('CB', 'centre-back'), ('RB', 'right-back'),
                       ('LM', 'left-midfield'), ('CM', 'centre-midfield'),
                       ('RM', 'right-midfield'), ('CF', 'centre-forward'),)
    # ToDo fill more positions

    position = models.CharField(max_length=3, choices=PositionChoices)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Competition(models.Model):
    TypeChoices = (('league', 'league'), ('tournament', 'tournament'),)

    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=10, choices=TypeChoices)
    area = models.CharField(max_length=50, )
    year = models.IntegerField()


class Match(models.Model):
    date = models.DateTimeField()
    main_referee = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=50)
    stadium = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    crest_uri = models.CharField(max_length=200, null=True)


class TeamInMatch(models.Model):
    is_host = models.BooleanField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
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
