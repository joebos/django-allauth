from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount import app_settings


class PinterestAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('id')

    def get_avatar_url(self):
        return self.account.extra_data.get('image').get("60x60").get("url")

    def to_str(self):
        dflt = super(PinterestAccount, self).to_str()
        name = self.account.extra_data.get('username', dflt)
        first_name = self.account.extra_data.get('first_name', None)
        last_name = self.account.extra_data.get('last_name', None)
        if first_name and last_name:
            name = first_name + ' ' + last_name
        return name

class PinterestProvider(OAuth2Provider):
    id = 'pinterest'
    # Name is displayed to ordinary users -- don't include protocol
    name = 'Pinterest'
    package = 'allauth.socialaccount.providers.pinterest'
    account_class = PinterestAccount

    def extract_uid(self, data):
        import json
        print json.dumps(data)

        return str(data['id'])

    def get_profile_fields(self):
        default_fields = ['id',
                          'username',
                          'first_name',
                          'last_name',
                          'bio',
                          'counts',
                          'image',
                          'created_at']
        fields = self.get_settings().get('PROFILE_FIELDS',
                                         default_fields)
        return fields

    def get_default_scope(self):
        scope = ["read_public", "write_public"]
        return scope

    def extract_common_fields(self, data):
        return dict(username=data.get("username"),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    avatar=data.get('image')

                    )

providers.registry.register(PinterestProvider)
