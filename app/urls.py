from django.conf.urls import url
from app import views

urlpatterns = [
    url('^teams$', views.TeamList.as_view()),
    url('^teams/(?P<pk>[0-9]+)$', views.TeamDetail.as_view()),
    #url('^teams$', )
]
