from allauth.socialaccount.providers.oauth.urls import default_urlpatterns

from .provider import EtsyProvider

urlpatterns = default_urlpatterns(EtsyProvider)
