from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount import app_settings


class SchedulePicturesOAuth2Account(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('id')

    def get_avatar_url(self):
        return self.account.extra_data.get('id')

    def to_str(self):
        dflt = super(SchedulePicturesOAuth2Account, self).to_str()
        name = self.account.extra_data.get('username', dflt)
        first_name = self.account.extra_data.get('first_name', None)
        last_name = self.account.extra_data.get('last_name', None)
        if first_name and last_name:
            name = first_name+' '+last_name
        return name


class SchedulePicturesOAuth2Provider(OAuth2Provider):
    id = 'schedulepictures_oauth2'
    # Name is displayed to ordinary users -- don't include protocol
    name = 'SchedulePictures'
    package = 'allauth.socialaccount.providers.schedulepictures_oauth2'
    account_class = SchedulePicturesOAuth2Account

    def extract_uid(self, data):
        return str(data['id'])

    def get_profile_fields(self):
        default_fields = ['id',
                          'first-name',
                          'last-name',
                          'email-address',
                          'picture-url',
                          'public-profile-url']
        fields = self.get_settings().get('PROFILE_FIELDS',
                                         default_fields)
        return fields

    def get_default_scope(self):
        scope = ["read", "write"]

        #if app_settings.QUERY_EMAIL:
        #    scope.append('r_emailaddress')
        return scope

    def extract_common_fields(self, data):
        return dict(username=data.get("username"),
                    email=data.get('email'),
                    #first_name=data.get('first_name'),
                    #last_name=data.get('last_name')
                    )


providers.registry.register(SchedulePicturesOAuth2Provider)
