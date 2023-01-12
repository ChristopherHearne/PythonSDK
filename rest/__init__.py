import os
import json
from urllib.parse import urlencode
import requests
from api_resources.api_requester import APIRequester
from api_resources.mixins.mixins import PathBuilder

class Client(object):
    """
    A client for accessing the Nuxt Project API.
    """

    def __init__(
            self,
            version=None,
            env=None,
            environ=None
    ):

        environ = environ or os.environ
        self.hedera_mirror_version = version or environ.get('hedera_mirror_VERSION')
        self.env = env or environ.get('hedera_mirror_ENV')

        base_url = {
            "main": "http://localhost:9362/api",
        }
        try:
            self.base_url = base_url[self.env.strip().lower()]
        except AttributeError:
            raise Exception("Use 'main as env")

        # Domains
        self._profile = None
        self._token = None

    def request(self, method, base_url, domain, version, profile_id=None,
                domain_id=None, domain_action=None, params=None, data=None, headers=None, auth=None):

        headers = headers or {}
        params = params or {}
        method = method.upper()

        path, url = PathBuilder(base_url=base_url, domain=domain, version=version, profile_id=profile_id,
                                domain_id=domain_id, domain_action=domain_action, params=params).build()

        print(f'Endpoint (url): \n{url}\n\n')

        api = APIRequester(url=url)

        if method == "POST":
            response = api.post()
        elif method == "GET":
            response = api.get()
        elif method == "PUT":
            response = api.put()
        elif method == "DELETE":
            response = api.delete()

        if method == "DELETE":
            print(
                f'Response:\nStatus:\n{response.status_code}\nJson Response:\n{response.json()}'
            )
            json_response = {}
        else:
            print(
                f'Response:\nStatus:\n{response.status_code}\nJson Response:\n{response.json()}'
            )
            json_response = response.json()
        return {
            "status": response.status_code,
            "json": json_response
        }

    @property
    def profile(self):
        """
        Access the sdk Profile API
        """
        if self._profile is None:
            from rest.profile import Profile
            self._profile = Profile(self, self.base_url, 'profiles', version="v1")
        return self._profile

    @property
    def token(self):
        """
        Access the sdk Token API
        """
        if self._token is None:
            from rest.token import Token
            self._token = Token(self, self.base_url, 'tokens', version="v1")
        return self._token
