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
    team_id = models.ForeignKey(related_name='players', on_delete=models.CASCADE)
