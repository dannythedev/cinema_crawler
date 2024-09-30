from uu import encode

import requests
from Parser import Parser

class Request:
    def __init__(self):
        self.rating = []
        self.html = Parser()
        self.home_url = NotImplemented
        self.headers = {}
        self.params = {}
        self.request_counter = 0
        self.xpaths = {key: [] for key in ['image', 'trailer', 'genre', 'year', 'duration', 'title', 'rating', 'screening']}
        self.name = None

    def get(self, url):
        response = requests.get(url=url, headers=self.headers, params=self.params)
        with open('response.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        self.request_counter += 1
        self.html.set(response)
        if response.status_code == 404:
            return
        return response