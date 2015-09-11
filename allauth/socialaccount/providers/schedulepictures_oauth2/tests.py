from allauth.socialaccount.tests import create_oauth2_tests
from allauth.tests import MockedResponse
from allauth.socialaccount.providers import registry

from .provider import SchedulePicturesOAuth2Provider


class SchedulePicturesOAuth2Tests(create_oauth2_tests(
        registry.by_id(SchedulePicturesOAuth2Provider.id))):

    def get_mocked_response(self):
        return MockedResponse(200, """
{
  "emailAddress": "raymond.penners@intenct.nl",
  "firstName": "Raymond",
  "id": "ZLARGMFT1M",
  "lastName": "Penners",
  "pictureUrl": "http://m.c.lnkd.licdn.com/mpr/mprx/0_e0hbvSLc",
  "publicProfileUrl": "http://www.schedulepictures.com/in/intenct"
}
""")
