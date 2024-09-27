import re

from Functions import exception_method, IMAGE_NOT_FOUND
from Reviewers.Reviewer import Reviewer


class RottenTomatoes(Reviewer):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.rottentomatoes.com/m/'
        self.xpaths.update({'image': ["//tile-dynamic[@class='thumbnail']//@src"],
                            'duration': ["//p[@class='info']/text()"],
                            'genre': ["//p[@class='info']/text()"],
                            'audience_score': ["//rt-button[@slot='audienceScore']/rt-text/text()"],
                            'critics_score': ["//rt-button[@slot='criticsScore']/rt-text/text()"],
                            'year': ["//p[@class='info']/text()"]})
        self.name = 'Rotten Tomatoes'

    @exception_method
    def get_duration(self, movie):
        if not movie.duration:
            movie.duration = self.html.get_xpath_element_by_index(self.xpaths['duration']).split(', ')[2]

    @exception_method
    def get_genre(self, movie):
        if not movie.genre:
            movie.genre = self.html.get_xpath_element_by_index(self.xpaths['genre']).split(', ')[1]

    @exception_method
    def get_year(self, movie):
        if not movie.year:
            movie.year = self.html.get_xpath_element_by_index(self.xpaths['year']).split(', ')[0]

    def get_attributes(self, movie, url=''):
        def check_if_has_numbers(string):
            return re.search(r'\d', string)
        validation = super().get_attributes(movie=movie, url=self.home_url + movie.suffix.replace('-', '_'))
        if validation:
            return
        critic_score = str(self.html.get_xpath_element_by_index(self.xpaths['critics_score']))
        audience_score = str(self.html.get_xpath_element_by_index(self.xpaths['audience_score']))
        if check_if_has_numbers(critic_score):
            movie.rating.update({'Tomatometer Audience Score': int(critic_score.replace('%', ''))})
        if check_if_has_numbers(audience_score):
            movie.rating.update({'Tomatometer Critic Score': int(audience_score.replace('%', ''))}),
        return
