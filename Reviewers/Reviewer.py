import datetime

from Functions import exception_method
from Request import Request

class Reviewer(Request):
    def __init__(self):
        self.progress = 0
        self.validate_year_first = False
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

    @exception_method
    def get_year(self, movie):
        pass

    def validate_year(self, movie):
        if movie.origin and movie.year:
            return int(movie.year) >= int((datetime.datetime.now() - datetime.timedelta(days=5 * 30)).date().strftime('%Y'))
        return True

    def get_attributes(self, movie, url=''):
        """Returns dictionary of ratings. None if it doesn't retrieve it."""
        if self.validate_year_first:
            self.get_year(movie)
            if not self.validate_year(movie):
                return True
            self.get(url)
        else:
            self.get(url)
            self.get_year(movie)
            if not self.validate_year(movie):
                return True
        self.get_duration(movie)
        self.get_genre(movie)
        self.get_image(movie)
        self.get_trailer(movie)
        return False

    def initialize(self, movies_list):
        for movie in movies_list:
            try:
                self.get_attributes(movie)
            except Exception as e:
                print(e)
                pass
            self.progress += 1
