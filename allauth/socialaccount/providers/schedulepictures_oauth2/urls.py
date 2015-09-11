from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import SchedulePicturesOAuth2Provider

urlpatterns = default_urlpatterns(SchedulePicturesOAuth2Provider)

