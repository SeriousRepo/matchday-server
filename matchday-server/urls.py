from rest_framework.documentation import include_docs_urls
from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('app.urls')),
    url(r'docs', include_docs_urls(title='Api Documentation'))
]
