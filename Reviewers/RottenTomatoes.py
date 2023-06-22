from Functions import exception_method, IMAGE_NOT_FOUND
from Reviewers.Reviewer import Reviewer


class RottenTomatoes(Reviewer):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.rottentomatoes.com/m/'
        self.xpaths.update({'image': ["//tile-dynamic[@class='thumbnail']//@src"],
                            'duration': ["//p[@class='info']/text()"],
                            'genre': ["//p[@class='info']/text()"],
                            'year': ["//p[@class='info']/text()"]})

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
        validation = super().get_attributes(movie=movie, url=self.home_url + movie.suffix.replace('-', '_'))
        if validation:
            return
        board = self.html.find("score-board")  # Rating
        if board is not None:
            if board["audiencescore"]:
                movie.rating['Tomatometer Audience Score'] = int(board["audiencescore"])
            if board["tomatometerscore"]:
                movie.rating['Tomatometer Critic Score'] = int(board["tomatometerscore"])
        return
