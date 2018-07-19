from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)

    class Meta:
        ordering = ('points',)


class Player(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)


class Match(models.Model):
    date = models.DateTimeField()
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
