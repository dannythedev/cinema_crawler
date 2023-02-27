from cinema.Reviewers.Reviewer import Reviewer


class RottenTomatoes(Reviewer):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.rottentomatoes.com/m/'

    def get_rating(self, movie):
        self.get(url=self.url + movie.suffix.replace('-', '_'))
        board = self.html.find("score-board")
        if board is not None:
            if board["audiencescore"] == '' and board["tomatometerscore"] == '':
                return
            movie.rating.update({'Tomatometer Audience Score': int(board["audiencescore"]),
                                 'Tomatometer Critic Score': int(board["tomatometerscore"])})
