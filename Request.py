import requests
from Parser import Parser

class Request:
    def __init__(self):
        self.rating = []
        self.html = Parser()
        self.url = NotImplemented
        self.headers = {}

    def get(self, url):
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 404:
            return
        self.html.set(response)
        return response

