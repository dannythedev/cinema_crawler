import json
import threading
from Cinemas.YesPlanet import YesPlanet
from Cinemas.CinemaCity import CinemaCity
from Cinemas.HotCinema import HotCinema
from Functions import capitalize_sentence
from Reviewers.IMDB import IMDB
from Reviewers.Metacritic import Metacritic
from Reviewers.RottenTomatoes import RottenTomatoes

EXPORT_FILE = 'movies.json'


class Archive:
    def __init__(self, checklist=[], is_screenings=False):
        self.current, self.total = 0, 0
        cinemas = []
        movies_dict = {'YesPlanet': YesPlanet(),
                       'CinemaCity': CinemaCity(),
                       'HotCinema': HotCinema()}
        for key in movies_dict.keys():
            if key in checklist:
                cinemas.append(movies_dict[key])
        self.movies = []
        for cinema in cinemas:
            exported_movies = cinema.get_movies()
            self.movies += exported_movies
            if is_screenings:
                cinema.set_movie_screenings(exported_movies)

        unique_list = dict()
        # Iterate over each item in the original list
        for item in self.movies:
            # Check if the item is already in the unique list
            if item.title not in list(unique_list.keys()):
                # If it's not, add it to the unique list
                unique_list.update({item.title: item})
            else:
                if str(item.origin) not in str(unique_list[item.title].origin):
                    unique_list[item.title].origin.update(item.origin)
                    for screening in item.screenings:
                        unique_list[item.title].screenings.update({screening: item.screenings[screening]})
                        # Sort list by time and remove duplicates.
                        unique_list[item.title].screenings[screening] = list(
                            set(unique_list[item.title].screenings[screening]))
                        unique_list[item.title].screenings[screening] = \
                            sorted(unique_list[item.title].screenings[screening],
                                   key=lambda x: (int(x.split(':')[0]), int(x.split(':')[1])))
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
        [setattr(movie, 'title', capitalize_sentence(movie.title)) for movie in self.movies]
        dumps = json.dumps([movie.__dict__ for movie in self.movies], indent=4)
        f = open(EXPORT_FILE, 'w')
        f.write(dumps)
        f.close()
