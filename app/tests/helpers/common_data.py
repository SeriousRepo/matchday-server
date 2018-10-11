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


def match(pk, referee=referee_person(1)):
    return MatchRepresentation(pk, referee.model, league_competition(1).model)


def event_info(pk, user):
    return EventInfoRepresentation(pk, user)


def match_team(pk, coach=coach_person(1), matchx=match(1)):
    return MatchTeamRepresentation(pk, team(1).model, matchx.model, coach.model)


def team_event(pk, user):
    return TeamEventRepresentation(pk=pk, player=player(1).model, match_team=match_team(1, coach_person(2)).model, event_info=event_info(pk, user).model)
