import requests
from allauth.socialaccount import providers
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from .provider import SchedulePicturesOAuth2Provider

class SchedulePicturesOAuth2Adapter(OAuth2Adapter):

    schedulepictures_url = "http://192.168.1.2:3600"

    provider_id = SchedulePicturesOAuth2Provider.id
    access_token_url = schedulepictures_url + '/oauth/token/'
    authorize_url = schedulepictures_url + '/oauth/authorize'
    profile_url = schedulepictures_url + '/users/~'
    supports_state = False

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_user_info(token)
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def get_user_info(self, token):
        fields = providers.registry \
            .by_id(SchedulePicturesOAuth2Provider.id) \
            .get_profile_fields()
        #url = self.profile_url + ':(%s)?format=json' % ','.join(fields)
        url = self.profile_url + '/?format=json'
        headers = {"Authorization": "bearer " + token.token}
        resp = requests.get(url, headers=headers)
        return resp.json()

oauth2_login = OAuth2LoginView.adapter_view(SchedulePicturesOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SchedulePicturesOAuth2Adapter)
