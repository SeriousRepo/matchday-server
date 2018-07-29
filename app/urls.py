from rest_framework import routers
from app import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'people', views.PersonViewSet, base_name='people')
router.register(r'players', views.PlayerViewSet)
router.register(r'matches', views.MatchViewSet, base_name='matches')
router.register(r'competitions', views.CompetitionViewSet, base_name='competitions')
router.register(r'competitions/(?P<competition_id>\d+)/matches',
                views.MatchPerCompetitionViewSet, base_name='competition')

urlpatterns = router.urls
