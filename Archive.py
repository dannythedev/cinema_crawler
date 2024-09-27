import datetime
import json
import threading

from Cinemas.LevCinema import LevCinema
from Cinemas.YesPlanet import YesPlanet
from Cinemas.CinemaCity import CinemaCity
from Cinemas.HotCinema import HotCinema
from Cinemas.YesVOD import YesVOD
from Functions import capitalize_sentence, IMAGE_NOT_FOUND, suffixify, compare_movie_names, validate_movie_titles
from Movie import Movie
from Reviewers.IMDB import IMDB
from Reviewers.Letterboxd import Letterboxd
from Reviewers.Metacritic import Metacritic
from Reviewers.RottenTomatoes import RottenTomatoes
from Reviewers.TheMovieDB import TheMovieDB

EXPORT_FILE = 'movies.json'


class Archive:
    def __init__(self, checklist=[], is_screenings=False, custom_search=None):
        self.progress = None
        self.current, self.total = 0, 0
        self.cinemas = []
        movies_dict = {'YesPlanet': YesPlanet(),
                       'CinemaCity': CinemaCity(),
                       'HotCinema': HotCinema(),
                       'LevCinema': LevCinema(),
                       'YesVOD': YesVOD()}
        for key in movies_dict.keys():
            if key in checklist:
                self.cinemas.append(movies_dict[key])
        self.movies = []
        self.checklist = checklist
        self.is_screenings = is_screenings
        self.custom_search = custom_search


    def initialize_cinemas(self):
        def update_movies():
            # Create a dictionary to store suffixes and their corresponding movies
            suffix_dict = {}
            def reduce_duplicate_similar_movie_titles():
                """Iterates over movie list. If there is an occurance of a duplicate movie with
                a different way of writing the title, it changes it to the longer title of the two,
                with the assumption the former gives more information out of reviewing sites."""
                for x in range(len(self.movies)):
                    for y in range(len(self.movies)):
                        if self.movies[x] != self.movies[y] and self.movies[x].suffix != self.movies[y].suffix:
                            if validate_movie_titles(self.movies[x].title, self.movies[y].title) or \
                                    compare_movie_names(self.movies[x].title, self.movies[y].title):
                                if len(self.movies[x].title) > len(self.movies[y].title):
                                    self.movies[y].suffix = self.movies[x].suffix
                                    self.movies[y].title = self.movies[x].title
                                else:
                                    self.movies[x].title = self.movies[y].title
                                    self.movies[x].title = self.movies[y].title

            reduce_duplicate_similar_movie_titles()

            # Iterate over the movie list
            for movie in self.movies:
                second_suffix = None
                skip_boolean = False
                for suffix in suffix_dict:
                    if compare_movie_names(movie.suffix, suffix):
                        skip_boolean = True
                        second_suffix = suffix_dict[suffix]
                # Check if the suffix already exists in the dictionary
                if movie.suffix in suffix_dict or skip_boolean:
                    # Get the existing movie with the same suffix
                    if movie.suffix in suffix_dict:
                        key = movie
                    else:
                        key = second_suffix
                    existing_movie = suffix_dict[key.suffix]
                    existing_movie.origin.update(key.origin)
                    existing_movie.screenings.update(key.screenings)

                    # Fuse the origin and screenings attributes
                    existing_movie.origin.update(movie.origin)
                    existing_movie.screenings.update(movie.screenings)
                else:
                    # Add the movie to the dictionary if the suffix doesn't exist
                    suffix_dict[movie.suffix] = movie
            # Return the updated list without duplicate suffixes
            return list(suffix_dict.values())

        if not self.custom_search:
            threads = []
            for x in range(len(self.cinemas)):
                thread = threading.Thread(target=self.cinemas[x].initialize, args=[self.is_screenings])
                thread.start()
                threads.append(thread)
            for x in range(len(threads)):
                threads[x].join()
                self.movies += self.cinemas[x].movies
            self.movies = update_movies()
            print('Requests:\n',([(cinema.name, cinema.request_counter) for cinema in self.cinemas]))
        else:
            self.movies = [Movie(title=self.custom_search, suffix=suffixify(self.custom_search), image=IMAGE_NOT_FOUND)]

        self.reviewers = []
        reviewers_dict = {'Metacritic': Metacritic(),
                          'RottenTomatoes': RottenTomatoes(),
                          'IMDB': IMDB(),
                          'TheMovieDB': TheMovieDB(),
                          'Letterboxd': Letterboxd()}
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
        print('Requests:\n',[(reviewer.name, reviewer.request_counter) for reviewer in self.reviewers])
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
        [setattr(movie, 'title', capitalize_sentence(movie.title)) for movie in self.movies]
        if self.is_screenings and not self.custom_search:
            # Shows only those with screenings.
            self.movies = [movie for movie in self.movies if movie.screenings]

        dumps = {'Movies': [movie.__dict__ for movie in self.movies],
                 'Date': datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")}
        dumps = json.dumps(dumps)
        f = open(EXPORT_FILE, 'w')
        f.write(dumps)
        f.close()
