import re

from Functions import convert_time, exception_method, IMAGE_NOT_FOUND
from Reviewers.Reviewer import Reviewer


class Metacritic(Reviewer):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.metacritic.com/movie/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        self.xpaths.update({'image': ["//img[@class='summary_img']/@src"],
                            'duration': ["//div[@class='runtime']/span[2]/text()"],
                            'genre': ["//div[@class='genres']/span[2]/span/text()"],
                            'audience_rating': ["(//div[contains(@class, 'productScoreInfo')]/div/div/div/span//text())[1]"],
                            'critic_rating': ["(//div[contains(@class, 'productScoreInfo')]/div/div/div/span//text())[2]"],
                            'trailer': ["//div[@id='videoContainer_wrapper']/@data-mcvideourl"]})
        self.name = 'Metacritic'

    @exception_method
    def get_trailer(self, movie):
        if not movie.trailer:
            movie.trailer = self.html.get_xpath_element_by_index(self.xpaths['trailer'])

    @exception_method
    def get_duration(self, movie):
        if not movie.duration:
            movie.duration = convert_time(self.html.get_xpath_element_by_index(self.xpaths['duration']))

    def get_attributes(self, movie, url=''):
        def check_if_has_numbers(string):
            return re.search(r'\d', string)
        validation = super().get_attributes(movie=movie, url=self.home_url + movie.suffix)
        if validation:
            return
        critic_score = str(self.html.get_xpath_element_by_index(self.xpaths['critic_rating']))
        audience_score = str(self.html.get_xpath_element_by_index(self.xpaths['audience_rating']))
        if check_if_has_numbers(critic_score):
            movie.rating.update({'Metacritic Audience Score': int(float(critic_score) * 10)})
        if check_if_has_numbers(audience_score):
            movie.rating.update({'Metacritic Critic Score': int(audience_score)}),
