import json

from allauth.socialaccount.providers.oauth.client import OAuth
from allauth.socialaccount.providers.oauth.views import (OAuthAdapter,
                                                         OAuthLoginView,
                                                         OAuthCallbackView)

from .provider import EtsyProvider


class EtsyAPI(OAuth):
    """
    Verifying twitter credentials
    """
    url = 'https://openapi.etsy.com/v2/users/__SELF__'
    url_avatar = 'https://openapi.etsy.com/v2/users/__SELF__/avatar/src'
    url_shops = 'https://openapi.etsy.com/v2/users/__SELF__/shops'
    url_profile = 'https://openapi.etsy.com/v2/users/__SELF__/profile'

    def get_user_info(self):
        user = json.loads(self.query(self.url))
        #user_avatar = json.loads(self.query(self.url_avatar))
        user_shops = json.loads(self.query(self.url_shops))
        user_profile = json.loads(self.query(self.url_profile))

        data = {"user": user["results"][0], "profile": user_profile["results"][0], "shops": user_shops["results"]}

        return data


class EtsyOAuthAdapter(OAuthAdapter):
    provider_id = EtsyProvider.id
    request_token_url = 'https://openapi.etsy.com/v2/oauth/request_token'
    access_token_url = 'https://openapi.etsy.com/v2/oauth/access_token'
    # Issue #42 -- this one authenticates over and over again...
    # authorize_url = 'https://api.twitter.com/oauth/authorize'
    authorize_url = 'https://www.etsy.com/oauth/signin'

    def complete_login(self, request, app, token):
        client = EtsyAPI(request, app.client_id, app.secret,
                            self.request_token_url)
        extra_data = client.get_user_info()
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)


oauth_login = OAuthLoginView.adapter_view(EtsyOAuthAdapter)
oauth_callback = OAuthCallbackView.adapter_view(EtsyOAuthAdapter)
