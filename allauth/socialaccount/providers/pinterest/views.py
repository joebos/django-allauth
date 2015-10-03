import requests
from allauth.socialaccount import providers
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from .provider import PinterestProvider

class PinterestAdapter(OAuth2Adapter):

    #pinterest_url = "http://192.168.1.17:3600"

    pinterest_url = "https://api.pinterest.com"


    provider_id = PinterestProvider.id
    access_token_url = pinterest_url + '/v1/oauth/token'
    authorize_url = pinterest_url + '/oauth/'
    profile_url = pinterest_url + '/v1/me/'
    supports_state = False

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_user_info(token)
        extra_data = extra_data["data"] if "data" in extra_data else None
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def get_user_info(self, token):
        fields = providers.registry \
            .by_id(PinterestProvider.id) \
            .get_profile_fields()
        url = self.profile_url + '?fields=%s' % ','.join(fields)
        headers = {"Authorization": "bearer " + token.token}

        import json
        print json.dumps(headers)
        print url

        resp = requests.get(url, headers=headers)
        return resp.json()

oauth2_login = OAuth2LoginView.adapter_view(PinterestAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(PinterestAdapter)
