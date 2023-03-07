import json


class Archive:
    def __init__(self, movies):
        self.movies = movies

    def sort_by_rating(self):
        """Calculates total rating for each movie in Archive, then sorts them by this value."""
        [movie.accumulate_rating() for movie in self.movies]
        self.movies = sorted(self.movies, key=lambda d: d.total_rating, reverse=True)

    def export_json(self):
        """Exports data as a JSON file."""
        dumps = json.dumps([movie.__dict__ for movie in self.movies], indent=4)
        file = open('movies.json', 'w')
        file.write(dumps)
        file.close()
