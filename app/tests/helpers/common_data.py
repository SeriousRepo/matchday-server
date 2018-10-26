from app.tests.helpers.data_representations import *


def league_competition(pk):
    return CompetitionRepresentation(pk, 'league', 2017)


def tournament_competition(pk):
    return CompetitionRepresentation(pk, 'tournament', 2017)


def wrong_type_competition(pk):
    return CompetitionRepresentation(pk, 'wrong_type', 2017)


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
    return PlayerRepresentation(pk, team(1).model, player_person(pk).model)


def match(pk, referee=referee_person(1)):
    return MatchRepresentation(pk, referee.model, league_competition(1).model)


def event_info(pk, user):
    return EventInfoRepresentation(pk, user)


def team_in_match(pk, coach=coach_person(1), matchx=match(1)):
    return TeamInMatchRepresentation(pk, team(1).model, matchx.model, coach.model)
