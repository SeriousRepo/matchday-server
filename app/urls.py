from rest_framework import routers
from app import views


router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet, base_name='users')
router.register(r'people', views.PersonsViewSet, base_name='people')
router.register(r'referees', views.RefereesViewSet, base_name='referees')
router.register(r'players', views.PlayersViewSet)
router.register(r'matches', views.MatchesViewSet, base_name='matches')
router.register(r'competitions', views.CompetitionsViewSet, base_name='competitions')
router.register(r'competitions/(?P<competition_id>\d+)/matches',
                views.MatchesPerCompetitionViewSet, base_name='matches_in_competition')
router.register(r'competitions/(?P<competition_id>\d+)/referees',
                views.RefereesPerCompetitionViewSet, base_name='referees_in_competition')
router.register(r'teams', views.TeamViewSet, base_name='teams')
router.register(r'match_team', views.MatchTeamViewSet, base_name='match_team')

urlpatterns = router.urls
