from rest_framework import routers
from app import views


router = routers.DefaultRouter(trailing_slash=False)
router.register('teams', views.TeamViewSet)
router.register('players', views.PlayerViewSet)
urlpatterns = router.urls
