from Functions import convert_time, exception_method, IMAGE_NOT_FOUND
from Reviewers.Reviewer import Reviewer


class Metacritic(Reviewer):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.metacritic.com/movie/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    @exception_method
    def get_image(self, movie):
        if movie.image == IMAGE_NOT_FOUND:
            xpath = str(self.html.get_xpath("//img[@class='summary_img']/@src")[0])
            if 'poster-default' not in xpath:
                movie.image = xpath

    @exception_method
    def get_trailer(self, movie):
        if not movie.trailer:
            movie.trailer = str(self.html.get_xpath("//div[@id='videoContainer_wrapper']/@data-mcvideourl")[0])

    @exception_method
    def get_duration(self, movie):
        if not movie.duration:
            movie.duration = convert_time(str(self.html.get_xpath("//div[@class='runtime']/span[2]/text()")[0]))

    @exception_method
    def get_genre(self, movie):
        if not movie.genre:
            movie.genre = str(', '.join(self.html.get_xpath("//div[@class='genres']/span[2]/span/text()")))

    def get_attributes(self, movie, url=''):
        validation = super().get_attributes(movie=movie, url=self.home_url + movie.suffix)
        if validation:
            return
        critic_score = self.html.get_xpath("//span[contains(@class, 'metascore_w larger movie')]/text()")[0]
        audience_score = self.html.get_xpath("//span[contains(@class, 'metascore_w user')]/text()")[0]
        movie.rating.update({'Metacritic Audience Score': int(critic_score),
                             'Metacritic Critic Score': int(float(audience_score) * 10)})
