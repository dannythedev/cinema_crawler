import json

import bs4

from Cinemas.Cinema import Cinema
from Functions import is_english
from Parser import regexify
from Movie import Movie
from lxml import etree

class CinemaCity(Cinema):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.cinema-city.co.il/home/MoviesGrid'
        self.params = {'cat': 'now', 'page': 0, 'TheaterId': 0, 'catId': 0}


    def get_movies(self):
        movies = []
        for x in range(0,12):
            self.params['page'] += 1
            response = super().get(self.url)
            movies += self.html.get_xpath("//div[@class='col-lg-3 col-md-4 col-sm-4 col-6 movie-thumb']")
        movies = [etree.tostring(x, pretty_print=True) for x in movies]
        movies_list = []
        for response_text in movies:
            dom = etree.HTML(str(bs4.BeautifulSoup(str(response_text), "html.parser")))
            title = dom.xpath("//div[@class='flip-1']/p[@class='sub-title']/text()") + dom.xpath("//div[@class='flip-1']/p[@class='title']/text()")
            if title:
                title = str(title[0])
                if is_english(title):
                    movies_list.append(Movie(title=title,
                                             suffix=title.replace(' ','-').lower(),
                                             trailer='',
                                             genre=[],
                                             image=dom.xpath("//img[@class='img-responsive flip-thumb']/@src"),
                                             origin='Cinema City')
                                             )
        return movies_list
