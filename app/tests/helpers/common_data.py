from app.tests.helpers.data_representations import *


def league_competition(pk):
    return CompetitionRepresentation(pk, 'league')


def tournament_competition(pk):
    return CompetitionRepresentation(pk, 'tournament')


def wrong_type_competition(pk):
    return CompetitionRepresentation(pk, 'wrong_type')


def referee_person(pk):
    return PersonRepresentation(pk, 'referee')


def coach_person(pk):
    return PersonRepresentation(pk, 'coach')


def player_person(pk):
    return PersonRepresentation(pk, 'player')


def wrong_type_person(pk):
    return PersonRepresentation(pk, 'wrong_type')


def team(pk, city='city'):
    return TeamRepresentation(pk, city)


def player(pk):
    return PlayerRepresentation(pk, team(pk).model, player_person(pk).model)


def match(pk):
    return MatchRepresentation(pk, referee_person(1).model, league_competition(1).model)


def event_info(pk, user):
    return EventInfoRepresentation(pk, user)
