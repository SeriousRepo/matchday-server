from rest_framework.documentation import include_docs_urls
from allauth.account.views import confirm_email
from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('app.urls')),
    url(r'docs', include_docs_urls(title='Api Documentation')),
    url(r'', include('rest_auth.urls')),
    url(r'registration/', include('rest_auth.registration.urls')),
    url(r'^registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]
