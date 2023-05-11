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

    def filter_categories_in_list(self, l):
        """Filters categories per self.filter_categories list."""
        return ', '.join([capitalize_sentence(x) for x in l if x.lower() in self.filter_categories])
