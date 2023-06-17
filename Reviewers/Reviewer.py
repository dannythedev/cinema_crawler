from Functions import exception_method
from Request import Request

class Reviewer(Request):
    def __init__(self):
        self.progress = 0
        super().__init__()

    @exception_method
    def get_duration(self, movie):
        pass

    @exception_method
    def get_genre(self, movie):
        pass

    @exception_method
    def get_image(self, movie):
        pass

    @exception_method
    def get_trailer(self, movie):
        pass

    def get_attributes(self, movie, url=''):
        """Returns dictionary of ratings. None if it doesn't retrieve it."""
        self.get(url)
        self.get_duration(movie)
        self.get_genre(movie)
        self.get_image(movie)
        self.get_trailer(movie)

    def initialize(self, movies_list):
        for movie in movies_list:
            try:
                self.get_attributes(movie)
            except:
                pass
            self.progress += 1
