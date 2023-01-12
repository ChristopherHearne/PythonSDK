import requests


class APIRequester:
    """
    Class that utilises the requests library to make GET, PUT, POST and DELETE operations
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
        return response

    def post(self):
        response = requests.post(
            self.url,
            self.data,
            headers=self.headers
        )
        return response

    def put(self):
        response = requests.put(
            self.url,
            self.data,
            headers=self.headers
        )
        return response
