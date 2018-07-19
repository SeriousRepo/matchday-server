from rest_framework import routers
from app import views


router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'teams/(?P<team_id>\d+)/players', views.PlayerPerTeamViewSet, base_name='team')
router.register(r'teams/(?P<team_id>\d+)/home_matches', views.HomeMatchPerTeamViewSet, base_name='team')
router.register(r'teams/(?P<team_id>\d+)/away_matches', views.AwayMatchPerTeamViewSet, base_name='team')
router.register(r'players', views.PlayerViewSet)
router.register(r'matches', views.MatchViewSet)
urlpatterns = router.urls
