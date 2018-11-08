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
router.register(r'coaches', views.CoachesViewSet, base_name='coaches')
router.register(r'players', views.PlayersViewSet, base_name='players')
router.register(r'matches', views.MatchesViewSet, base_name='matches')
router.register(r'competitions', views.CompetitionsViewSet, base_name='competitions')
router.register(r'competitions/(?P<competition_id>\d+)/matches',
                views.MatchesPerCompetitionViewSet, base_name='matches_in_competition')
router.register(r'competitions/(?P<competition_id>\d+)/referees',
                views.RefereesPerCompetitionViewSet, base_name='referees_in_competition')
router.register(r'teams', views.TeamsViewSet, base_name='teams')
router.register(r'teams_in_matches', views.TeamsInMatchesViewSet, base_name='teams_in_matches')
router.register(r'match_events', views.MatchEventsViewSet, base_name='match_events')
router.register(r'team_events', views.TeamEventsViewSet, base_name='team_events')

urlpatterns += router.urls
