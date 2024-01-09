import json
import datetime

from Functions import exception_method, IMAGE_NOT_FOUND, suffixify, regexify, REGEX_RATING
from Reviewers.Reviewer import Reviewer


class IMDB(Reviewer):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.imdb.com/'
        self.search_url = 'https://www.imdb.com/find/?q='
        self.search_api_url = 'https://v3.sg.media-imdb.com/suggestion/x/{query}.json?includeVideos=1'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        self.validate_year_first = True
        self.xpaths.update({'image': ["//div[@class='sc-61c73608-1 jLwVZW']//@src"],
                            'duration': ["//li[@class='ipc-inline-list__item']/text()"],
                            'genre': ["//div[@class='ipc-chip-list__scroller']/a//text()"],
                            'trailer': ["//section[@data-testid='videos-section']//div[@role='group']//@href"],
                            'year': ["//section/div[2]/div[1]/ul/li[1]/a/text()"],
                            'rating': ["//span[contains(@class, 'sc-bde20123-1')]/text()"]})
        self.name = 'IMDB'

    @exception_method
    def get_duration(self, movie):
        if not movie.duration:
            movie.duration = self.html.get_xpath_element_by_index(self.xpaths['duration'])

    @exception_method
    def get_trailer(self, movie):
        if not movie.trailer:
            movie.trailer = self.home_url+\
                            self.html.get_xpath_element_by_index(self.xpaths['trailer'])


    def get_attributes(self, movie, url=''):
        response = self.get(self.search_api_url.format(query=suffixify(movie.title)))
        response = json.loads(response.text)['d']
        for query in response:
            if suffixify(query['l']) == movie.suffix and query['qid'] == 'movie':
                movie.year = query['y']
                movie.image = query['i']['imageUrl']
                validation = super().get_attributes(movie, url=self.home_url +'title/'+ query['id'])
                if validation:
                    continue

            rating = self.html.get_xpath_element_by_index(self.xpaths['rating'])
            movie.rating.update({'IMDB Audience Score': int(float(rating) * 10)})
            return
