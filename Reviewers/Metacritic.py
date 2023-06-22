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
            xpath = self.html.get_xpath_element_by_index("//img[@class='summary_img']/@src")
            if 'poster-default' not in xpath:
                movie.image = xpath

    @exception_method
    def get_trailer(self, movie):
        if not movie.trailer:
            movie.trailer = self.html.get_xpath_element_by_index("//div[@id='videoContainer_wrapper']/@data-mcvideourl")

    @exception_method
    def get_duration(self, movie):
        if not movie.duration:
            movie.duration = convert_time(self.html.get_xpath_element_by_index("//div[@class='runtime']/span[2]/text()"))

    @exception_method
    def get_genre(self, movie):
        if not movie.genre:
            movie.genre = ', '.join(self.html.get_xpath_elements("//div[@class='genres']/span[2]/span/text()"))

    def get_attributes(self, movie, url=''):
        validation = super().get_attributes(movie=movie, url=self.home_url + movie.suffix)
        if validation:
            return
        critic_score = self.html.get_xpath_element_by_index("//span[contains(@class, 'metascore_w larger movie')]/text()")
        audience_score = self.html.get_xpath_element_by_index("//span[contains(@class, 'metascore_w user')]/text()")
        movie.rating.update({'Metacritic Audience Score': int(critic_score),
                             'Metacritic Critic Score': int(float(audience_score) * 10)})
