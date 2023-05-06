import requests
from Parser import Parser

class Request:
    def __init__(self):
        self.rating = []
        self.html = Parser()
        self.url = NotImplemented
        self.headers = {}
        self.params = {}

    def get(self, url):
        response = requests.get(url=url, headers=self.headers, params=self.params)
        self.html.set(response)
        if response.status_code == 404:
            return
        return response

