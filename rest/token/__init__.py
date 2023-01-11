
# coding=utf-8
class Token:
    def __init__(self, sdk, base_url, domain, version, **kwargs):
        """
        Initialize the Account Domain
        :param sdk:
        :param base_url:
        :param domain:
        :param version:
        :param kwargs:
        """

        super(Token, self)
        self.sdk = sdk
        self.base_url = base_url
        self.domain = domain
        self.version = version

    def get(self, params=None, data=None, headers=None, auth=None, profile_id=None, domain_id=None, domain_action=None):
        return self.sdk.request(
            'get',
            self.base_url,
            self.domain,
            self.version,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            profile_id=profile_id,
            domain_id=domain_id,
            domain_action=domain_action
        )
