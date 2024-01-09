class Movie:
    def __init__(self, title, suffix, image, trailer='', genre='', origin=None, year=None, url=None):
        self.title = title
        self.total_rating = 0
        self.image = image
        self.duration = None
        self.rating = dict()
        self.genre = genre
        self.suffix = suffix
        self.trailer = trailer
        self.origin = origin
        self.screenings = {}
        self.year = year
        self.url = url

    def accumulate_rating(self):
        """Calculates rating average out of all reviewer scores."""
        if len(self.rating) != 0:
            self.total_rating = sum([self.rating[key] for key in self.rating if self.rating[key]])/len(self.rating)
