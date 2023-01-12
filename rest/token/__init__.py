# coding=utf-8
from api_resources.abstract.domain import Domain


class Token(Domain):
    def __init__(self, sdk, base_url, domain, version, **kwargs):
        """
        Initialize the Account Domain
        :param sdk:
        :param base_url:
        :param domain:
        :param version:
        :param kwargs:
        """

        super(Token, self).__init__(sdk)
        self.sdk = sdk
        self.base_url = base_url
        self.domain = domain
        self.version = version
