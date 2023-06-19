import json
import threading
from Cinemas.YesPlanet import YesPlanet
from Cinemas.CinemaCity import CinemaCity
from Cinemas.HotCinema import HotCinema
from Functions import capitalize_sentence, IMAGE_NOT_FOUND, suffixify
from Movie import Movie
from Reviewers.IMDB import IMDB
from Reviewers.Metacritic import Metacritic
from Reviewers.RottenTomatoes import RottenTomatoes

EXPORT_FILE = 'movies.json'


class Archive:
    def __init__(self, checklist=[], is_screenings=False, custom_search=None):
        self.current, self.total = 0, 0
        self.cinemas = []
        movies_dict = {'YesPlanet': YesPlanet(),
                       'CinemaCity': CinemaCity(),
                       'HotCinema': HotCinema()}
        for key in movies_dict.keys():
            if key in checklist:
                self.cinemas.append(movies_dict[key])
        self.movies = []
        self.checklist = checklist
        self.is_screenings = is_screenings
        self.custom_search = custom_search


    def initialize_cinemas(self):
        def update_movies(movie_list):
            # Create a dictionary to store suffixes and their corresponding movies
            suffix_dict = {}

            # Iterate over the movie list
            for movie in movie_list:
                # Check if the suffix already exists in the dictionary
                if movie.suffix in suffix_dict:
                    # Get the existing movie with the same suffix
                    existing_movie = suffix_dict[movie.suffix]

                    # Fuse the origin and screenings attributes
                    existing_movie.origin.update(movie.origin)
                    existing_movie.screenings.update(movie.screenings)

                else:
                    # Add the movie to the dictionary if the suffix doesn't exist
                    suffix_dict[movie.suffix] = movie

            # Return the updated list without duplicate suffixes
            return list(suffix_dict.values())

        if not self.custom_search:
            for cinema in self.cinemas:
                exported_movies = cinema.get_movies()
                self.movies += exported_movies
                if self.is_screenings:
                    cinema.set_movie_screenings(exported_movies)
            self.movies = update_movies(self.movies)
        else:
            self.movies = [Movie(title=self.custom_search, suffix=suffixify(self.custom_search), image=IMAGE_NOT_FOUND, trailer='', genre=None, origin=None)]

        self.reviewers = []
        reviewers_dict = {'Metacritic': Metacritic(),
                          'RottenTomatoes': RottenTomatoes(),
                          'IMDB': IMDB()}
        for key in reviewers_dict.keys():
            if key in self.checklist:
                self.reviewers.append(reviewers_dict[key])
        self.progress = 0

    def initialize_reviewers(self):
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

    def get_reviewers_progress(self):
        """Gets progress of current pages scanned against total pages."""
        current = sum([reviewer.progress for reviewer in self.reviewers])
        total = len(self.movies) * (len(self.reviewers))
        return {'progress': int(current / total * 100) if total != 0 else 100, 'current':current, 'total':total}

    def get_movie_screenings_progress(self):
        current = sum([cinema.progress for cinema in self.cinemas])
        total = sum([cinema.total_progress for cinema in self.cinemas])
        return {'progress': int(current / total * 100) if total != 0 else 0, 'current':current, 'total':total}

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
