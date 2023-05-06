import json
import threading
from Cinemas.YesPlanet import YesPlanet
from Cinemas.CinemaCity import CinemaCity
from Cinemas.HotCinema import HotCinema
from Reviewers.IMDB import IMDB
from Reviewers.Metacritic import Metacritic
from Reviewers.RottenTomatoes import RottenTomatoes
EXPORT_FILE = 'movies.json'

class Archive:
    def __init__(self, checklist=[]):
        self.current, self.total = 0, 0
        cinemas = []
        movies_dict = {'CinemaCity': CinemaCity(),
                       'YesPlanet': YesPlanet(),
                       'HotCinema': HotCinema()}
        for key in movies_dict.keys():
            if key in checklist:
                cinemas.append(movies_dict[key])
        self.movies = []
        for cinema in cinemas:
            self.movies += cinema.get_movies()

        unique_list = dict()
        # Iterate over each item in the original list
        for item in self.movies:
            # Check if the item is already in the unique list
            if item.title not in list(unique_list.keys()):
                # If it's not, add it to the unique list
                unique_list.update({item.title : item})
            else:
                if item.origin not in unique_list[item.title].origin:
                    unique_list[item.title].origin += ', '+item.origin
        self.movies = list(unique_list.values())

        self.reviewers = []
        reviewers_dict = {'Metacritic': Metacritic(),
                          'RottenTomatoes': RottenTomatoes(),
                          'IMDB': IMDB()}
        for key in reviewers_dict.keys():
            if key in checklist:
                self.reviewers.append(reviewers_dict[key])
        self.progress = 0

    def initialize(self):
        """Initializes the module."""
        self.get_movies_data()
        self.sort_by_rating()
        self.export_json()

    def get_movies_data(self):
        """Gets the movie data from all the critics."""
        threads = []
        for reviewer in self.reviewers:
            thread = threading.Thread(target=reviewer.initialize, args=[self.movies])
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        # for reviewer in self.reviewers:
        #     reviewer.initialize(self.movies)

    def get_progress(self):
        """Gets progress of current pages scanned against total pages."""
        self.current = sum([reviewer.progress for reviewer in self.reviewers])
        self.total = len(self.movies) * (len(self.reviewers))
        return int(self.current / self.total * 100) if self.total != 0 else 100

    def sort_by_rating(self):
        """Calculates total rating for each movie in Archive, then sorts them by this value."""
        [movie.accumulate_rating() for movie in self.movies]
        self.movies = sorted(self.movies, key=lambda d: d.total_rating, reverse=True)

    def export_json(self):
        """Exports data as a JSON file."""
        [delattr(movie, 'suffix') for movie in self.movies]
        dumps = json.dumps([movie.__dict__ for movie in self.movies], indent=4)
        f = open(EXPORT_FILE, 'w')
        f.write(dumps)
        f.close()
