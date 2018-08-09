from rest_framework.documentation import include_docs_urls
from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('app.urls')),
    url(r'docs', include_docs_urls(title='Api Documentation')),
    url(r'', include('rest_auth.urls')),
    url(r'registration/', include('rest_auth.registration.urls')),
]
