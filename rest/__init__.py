import os
import json
from urllib.parse import urlencode
import requests


def create_params(**kwargs):
    """
    Used to create url parameters for API call
    :param kwargs:
    :return:
    """

    url = kwargs.get("url")
    params = kwargs.get("params")
    if params:
        query_string = urlencode(eval(params))
    return f'{url}?{query_string}'


class PathBuilder:
    """
    Used to build the correct API path that includes
    parameters & filters
    """

    def __init__(self, **kwargs):
        self.base_url = kwargs.get('base_url')
        self.domain = kwargs.get('domain')
        self.version = kwargs.get('version')
        self.profile_id = kwargs.get("profile_id")
        self.domain_id = kwargs.get("domain_id")
        self.domain_action = kwargs.get("domain_action")
        self.params = kwargs.get('params')

    def build(self):
        paths = {
            "domains": {
                "account": {
                    "path": 'api/Profile',
                    "name": None
                },
                "profiles": {
                    "path": 'api/Profile/profiles',
                    "name": None
                },
                "token": {
                    "path": 'tokens',
                    "name": None
                }
            }
        }
        domain_info = paths['domains'][self.domain]
        sections = [domain_info['path']]
        if self.profile_id:
            sections.append(self.profile_id)
        if domain_info["name"]:
            sections.append(domain_info["name"])
            if self.domain_id:
                sections.append(self.domain_id)
                if self.domain_action:
                    sections.append(self.domain_action)

        path = f'/{"/".join(sections)}'
        url = f'{self.base_url}{path}'

        # manage params and filtering
        params = {}
        operators = ["e", "lt", "lte", "gt", "gte"]
        for param in self.params.keys():
            if param in operators:
                params['account.id'] = f'{param}:{self.params[param]}'
            else:
                params[param] = self.params[param]
        if params:
            url = create_params(params=json.dumps(params), url=url)

        return [path, url]


class APIRequester:
    """
    Used to make the request
    """

    def __init__(self, **kwargs):
        self.method = kwargs.get("method")
        self.url = kwargs.get("url")
        self.headers = kwargs.get("headers")
        self.data = kwargs.get("data")

    def get(self):
        response = requests.get(
            self.url,
            headers=self.headers,
        )
        return response

    def delete(self):
        response = requests.delete(
            self.url,
            headers=self.headers
        )


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
            "main": "http://localhost:9362",
        }
        try:
            self.base_url = base_url[self.env.strip().lower()]
        except AttributeError:
            raise Exception("Use 'main as env")

        # Domains
        self._account = None

    def request(self, method, base_url, domain, version, profile_id=None,
                domain_id=None, domain_action=None, params=None, data=None, headers=None, auth=None):

        headers = headers or {}
        params = params or {}
        method = method.upper()

        path, url = PathBuilder(base_url=base_url, domain=domain, version=version, profile_id=profile_id,
                                domain_id=domain_id, domain_action=domain_action, params=params).build()

        print(f'Endpoint (url): \n{url}\n\n')
        api = APIRequester(url=url)
        response = api.get()

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
        if self._account is None:
            from rest.account import Profile
            self._account = Profile(self, self.base_url, 'token', self.hedera_mirror_version)
        return self._account
