from Functions import capitalize_sentence
from Request import Request


class Cinema(Request):
    filter_categories = ['comedy', 'action', 'adventure', 'horror', 'drama', 'romance', 'opera', 'israeli', 'thriller',
                         'crime', 'foreign', 'musical', 'sci-fi', 'kids']

    def __init__(self):
        super().__init__()

    def get_movies(self):
        """Returns a list of dictionaries with movie attributes."""
        pass
    def set_movie_screenings(self, movies):
        theatres = self.get_nearest_theatres()
        timetables = self.get_theatre_screenings(theatres, movies)
        self.place_screenings_under_movie_by_id(timetables, movies)

    def get_nearest_theatres(self):
        pass

    def get_theatre_screenings(self, theatres, movies=None):
        pass

    def place_screenings_under_movie_by_id(self, timetables, movies):
        """Places screenings under selected movie."""
        if timetables is None:
            return None
        for movie in movies:
            for timetable in timetables.keys():
                if movie.origin[self.name] in timetables[timetable]:
                    movie.screenings.update({timetable : timetables[timetable][movie.origin[self.name]]})

    def filter_categories_in_list(self, l):
        """Filters categories per self.filter_categories list."""
        return ', '.join([capitalize_sentence(x) for x in l if x.lower() in self.filter_categories])

