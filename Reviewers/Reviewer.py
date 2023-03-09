from Request import Request


class Reviewer(Request):
    def __init__(self):
        self.progress = 0
        super().__init__()

    def get_rating(self, movie):
        """Returns dictionary of ratings. None if it doesn't retrieve it."""
        pass

    def initialize(self, movies_list):
        for movie in movies_list:
            try:
                self.get_rating(movie)
                self.progress += 1
            except:
                pass
