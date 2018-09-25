from rest_framework.reverse import reverse
from rest_framework import status
from app.models import MatchTeam
from app.tests.tests_setup_base import TestsSetUpBase
from app.tests.data_representations import (TeamRepresentation, MatchRepresentation,
                                            PersonRepresentation, MatchTeamRepresentation)


"""class MatchTeamTestSetUp(TestsSetUpBase):
    base_url = reverse('match_teams-list')
    competition1 = CompetitionRepresentation(1, 'league')
    competition2 = CompetitionRepresentation(2, 'tournament')
    coach = PersonRepresentation(1, 'coach')
    match1 = MatchRepresentation(1, referee.model, competition1.model)
    match2 = MatchRepresentation(2, referee.model, competition2.model)
    updated_match = MatchRepresentation(1, referee.model, competition2.model)

    def post_nested(self, person=referee):
        self.register_user()
        self.post_method(reverse('people-list'), person.json)
        self.post_method(reverse('competitions-list'), self.competition1.json)
        self.post_method(reverse('competitions-list'), self.competition2.json)

    def post_single_match(self):
        self.post_nested()
        self.post_method(self.base_url, self.match1.json)

    def post_two_matches(self):
        self.post_nested()
        self.post_method(self.base_url, self.match1.json)
        self.post_method(self.base_url, self.match2.json)

    def get_nth_element_url(self, n):
        return self.get_specific_url(self.base_url, n)



"""