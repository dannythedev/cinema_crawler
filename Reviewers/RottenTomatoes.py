from Reviewers.Reviewer import Reviewer


class RottenTomatoes(Reviewer):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.rottentomatoes.com/m/'

    def get_duration(self, movie):
        try:
            if not movie.duration:
                movie.duration = str(self.html.get_xpath("//p[@class='info']/text()")[0].split(', ')[2])
        except:
            pass

    def get_attributes(self, movie):
        self.get(url=self.url + movie.suffix.replace('-', '_'))
        self.get_duration(movie)
        board = self.html.find("score-board") # Rating
        if board is not None:
            if board["audiencescore"] == '' and board["tomatometerscore"] == '':
                return
            movie.rating.update({'Tomatometer Audience Score': int(board["audiencescore"]),
                                 'Tomatometer Critic Score': int(board["tomatometerscore"])})
