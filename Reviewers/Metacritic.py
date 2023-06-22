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
                            'audience_rating': ["//span[contains(@class, 'metascore_w user')]/text()"],
                            'critic_rating': ["//span[contains(@class, 'metascore_w larger movie')]/text()"],
                            'trailer': ["//div[@id='videoContainer_wrapper']/@data-mcvideourl"]})

    @exception_method
    def get_trailer(self, movie):
        if not movie.trailer:
            movie.trailer = self.html.get_xpath_element_by_index(self.xpaths['trailer'])

    @exception_method
    def get_duration(self, movie):
        if not movie.duration:
            movie.duration = convert_time(self.html.get_xpath_element_by_index(self.xpaths['duration']))

    def get_attributes(self, movie, url=''):
        validation = super().get_attributes(movie=movie, url=self.home_url + movie.suffix)
        if validation:
            return
        critic_score = self.html.get_xpath_element_by_index(self.xpaths['critic_rating'])
        audience_score = self.html.get_xpath_element_by_index(self.xpaths['audience_rating'])
        movie.rating.update({'Metacritic Audience Score': int(critic_score),
                             'Metacritic Critic Score': int(float(audience_score) * 10)})
