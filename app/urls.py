from django.conf.urls import url
from rest_framework import routers
from app import views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    url(r'registration/$', views.UserCreateView.as_view(), name='account-create'),
    url(r'get_token/$', rest_views.obtain_auth_token)
]

router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet, base_name='users')
router.register(r'people', views.PeopleViewSet, base_name='people')
router.register(r'referees', views.RefereesViewSet, base_name='referees')
router.register(r'players', views.PlayersViewSet, base_name='players')
router.register(r'matches', views.MatchesViewSet, base_name='matches')
router.register(r'competitions', views.CompetitionsViewSet, base_name='competitions')
router.register(r'competitions/(?P<competition_id>\d+)/matches',
                views.MatchesPerCompetitionViewSet, base_name='matches_in_competition')
router.register(r'competitions/(?P<competition_id>\d+)/referees',
                views.RefereesPerCompetitionViewSet, base_name='referees_in_competition')
router.register(r'teams', views.TeamsViewSet, base_name='teams')
router.register(r'match_team', views.MatchTeamsViewSet, base_name='match_teams')
router.register(r'match_events', views.MatchEventsViewSet, base_name='match_events')
router.register(r'team_events', views.TeamEventsViewSet, base_name='team_events')
router.register(r'goals', views.GoalsViewSet, base_name='goals')
router.register(r'red_cards', views.RedCardsViewSet, base_name='red_cards')
router.register(r'yellow_cards', views.YellowCardsViewSet, base_name='yellow_cards')
router.register(r'substitutions', views.SubstitutionsViewSet, base_name='substitutions')
router.register(r'assists', views.AssistsViewSet, base_name='assists')

urlpatterns += router.urls
