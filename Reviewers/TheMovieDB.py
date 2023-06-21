from Functions import exception_method, IMAGE_NOT_FOUND, suffixify, regexify
from Reviewers.Reviewer import Reviewer


class TheMovieDB(Reviewer):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.themoviedb.org/'
        self.search_url = '{home_url}search/movie?query='.format(home_url=self.home_url)
        self.headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 ('
                                     'KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'}
    @exception_method
    def get_image(self, movie):
        if movie.image == IMAGE_NOT_FOUND:
            movie.image = self.home_url[:-1]+str(self.html.get_xpath("//div[@class='image_content backdrop']//@data-src")[0])

    @exception_method
    def get_duration(self, movie):
        if not movie.duration:
            movie.duration = str(self.html.get_xpath("//span[@class='runtime']/text()")[0])

    @exception_method
    def get_genre(self, movie):
        if not movie.genre:
            movie.genre = str(', '.join(self.html.get_xpath("//span[@class='genres']//a/text()")))

    @exception_method
    def get_trailer(self, movie):
        if not movie.trailer:
            movie.trailer = 'https://www.youtube.com/watch?v={id}'\
                .format(id=str(self.html.get_xpath("//div[@class='video card no_border']//a[@class='no_click play_trailer']/@data-id")[0]))

    def get_attributes(self, movie, url=''):
        """Searches for movie in IMDB. Then gets rating."""
        response = self.get(self.search_url + movie.title)

        movie_lists = dict(zip(self.html.get_xpath("//div[@class='title']/div/a[@data-media-type='movie']//text()"),
                  self.html.get_xpath("//div[@class='title']/div/a[@data-media-type='movie']//@href")))

        for results in movie_lists:
            if suffixify(movie.title) == suffixify(results):
                super().get_attributes(movie, url=self.home_url[:-1] + movie_lists[results])
                rating = regexify(r'\d+',self.html.get_xpath("//div[@class='percent']//@class")[1])
                movie.rating.update({'TheMovieDB Score': int(float(rating))})
                break