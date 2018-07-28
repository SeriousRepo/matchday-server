from rest_framework import routers
from app import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'people', views.PersonViewSet, base_name='people')
router.register(r'players', views.PlayerViewSet)
router.register(r'matches', views.MatchViewSet)
router.register(r'competitions', views.CompetitionViewSet)
router.register(r'competitions/(?P<competition_id>\d+)/matches',
                views.MatchPerCompetitionViewSet, base_name='competition')

urlpatterns = router.urls
