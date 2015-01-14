from allauth.account.models import EmailAddress
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import (ProviderAccount,
                                                  AuthAction)
from allauth.socialaccount.providers.oauth.provider import OAuthProvider


class EtsyAccount(ProviderAccount):
    def get_username(self):
        return self.account.extra_data.get('profile').get("login_name")

    def get_profile_url(self):
        ret = None
        username = self.get_username()
        if username:
            ret = 'https://www.etsy.com/people/' + username
        return ret

    def get_avatar_url(self):
        ret = None
        profile_image_url = self.account.extra_data.get('profile').get("image_url_75x75")
        if profile_image_url:
            # Hmm, hack to get our hands on the large image.  Not
            # really documented, but seems to work.
            ret = profile_image_url.replace('_normal', '')
        return ret

    def to_str(self):
        username = self.get_username()
        return username or super(EtsyAccount, self).to_str()


class EtsyProvider(OAuthProvider):
    id = 'etsy'
    name = 'etsy'
    package = 'allauth.socialaccount.providers.etsy'
    account_class = EtsyAccount

    def get_auth_url(self, request, action):
        if action == AuthAction.REAUTHENTICATE:
            url = 'https://www.etsy.com/oauth/sign'
        else:
            url = 'https://www.etsy.com/oauth/signin'
        return url

    def extract_uid(self, data):
        return data["profile"]['user_id']

    def extract_common_fields(self, data):
        return dict(username=data.get("profile").get("login_name"),
                    name=data.get("profile").get("first_name") + " " + data.get("profile").get("last_name"),
                    email=data.get("user").get("primary_email"))

    def extract_email_addresses(self, data):
        ret = []
        email = data.get('user').get("primary_email")
        if email:
            settings = self.get_settings()
            # data['verified'] does not imply the email address is
            # verified.
            verified_email = settings.get('VERIFIED_EMAIL', False)
            ret.append(EmailAddress(email=email,
                                    verified=verified_email,
                                    primary=True))
        return ret

    def get_default_scope(self):
        return ["email_r", "profile_r"]

providers.registry.register(EtsyProvider)
