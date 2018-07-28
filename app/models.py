from django.db import models


class User(models.Model):
    email = models.CharField(max_length=100)
    hash_password = models.CharField(max_length=250)
    join_date = models.DateField()
    rank_points = models.IntegerField()


class Person(models.Model):
    RoleChoices = (('coach', 'coach'), ('player', 'player'), ('referee', 'referee'),)

    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=RoleChoices)
    birth_date = models.DateField()


class Player(models.Model):
    PositionChoices = (('goalkeeper', 'GK'), ('left-back', 'LB'),
                       ('centre-back', 'CB'), ('right-back', 'RB'),
                       ('left-midfield', 'LM'), ('centre-midfield', 'CM'),
                       ('right-midfield', 'RM'), ('centre-forward', 'CF'),)
    # ToDo fill more positions

    position = models.CharField(max_length=3, choices=PositionChoices)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    # ? team = models.ForeignKey('Team', related_name='players', on_delete=models.CASCADE)


class Competition(models.Model):
    TypeChoices = (('league', 'league'), ('tournament', 'tournament'),)

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TypeChoices)


class Match(models.Model):
    date = models.DateTimeField()
    main_referee = models.OneToOneField('Person', on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name='matches', on_delete=models.CASCADE)
