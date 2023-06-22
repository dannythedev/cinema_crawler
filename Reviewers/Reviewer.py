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
        """Attaches duration string from self.html xpath to movie."""
        pass

    @exception_method
    def get_genre(self, movie):
        """Attaches genre string from self.html xpath to movie."""
        pass

    @exception_method
    def get_image(self, movie):
        """Attaches image URL from self.html xpath to movie."""
        pass

    @exception_method
    def get_trailer(self, movie):
        """Attaches trailer URL from self.html xpath to movie."""
        pass

    @exception_method
    def get_year(self, movie):
        """Attaches year from self.html xpath to movie."""
        pass

    def validate_by_year(self, movie):
        """Function that rules out movie ratings for movies with same name but different release years.
        Gets movie, checks if it has a Cinema origin. If it does, then it's likely first premiered less than 5 months ago.
        Compare this to movie release date, if it is not in range then return False. If it has no scrapped release date
        or a cinema origin, then do not validate."""
        if movie.origin and movie.year:
            return int(movie.year) >= int((datetime.datetime.now() - datetime.timedelta(days=5 * 30)).date().strftime('%Y'))
        return True

    def get_attributes(self, movie, url=''):
        """Collects rating attirubte for movie in Reviewer. Also collects other attributes like image, trailer, genre and duration,
        if they had not been collected from the Cinema."""
        if self.validate_year_first:
            self.get_year(movie)
            if not self.validate_by_year(movie):
                return True
            self.get(url)
        else:
            self.get(url)
            self.get_year(movie)
            if not self.validate_by_year(movie):
                return True
        self.get_duration(movie)
        self.get_genre(movie)
        self.get_image(movie)
        self.get_trailer(movie)
        return False

    def initialize(self, movies_list):
        """Gets movie list. Gets the attributes for each movie."""
        for movie in movies_list:
            try:
                self.get_attributes(movie)
            except Exception as e:
                print(e)
                pass
            self.progress += 1
