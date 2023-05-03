import json

import bs4
from Cinemas.Cinema import Cinema
from Functions import is_english, regexify
from Movie import Movie
from lxml import etree

class HotCinema(Cinema):
    def __init__(self):
        super().__init__()
        self.url = 'https://hotcinema.co.il/'

    def get_movies(self):
        response = super().get(self.url)
        movies = json.loads(regexify(regex='app.movies = (.*])', data=response.text))
        movies_list = []
        for x in movies:
            title = regexify(regex='/movie/\d*/(.*)', data=x['PageUrl'])
            if is_english(title):
                movies_list.append(Movie(title=title.replace('-', ' ').lower(),
                          suffix=title,
                          image='',
                          trailer='',
                          genre=[],
                          origin='Hot Cinema'))
        return movies_list