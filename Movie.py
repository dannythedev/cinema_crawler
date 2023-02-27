class Movie:
    def __init__(self, title, suffix, image, trailer, genre):
        self.title = title
        self.suffix = suffix
        self.image = image
        self.trailer = trailer
        self.total_rating = 0
        self.rating = dict()
        self.genre = genre

    def accumulate_rating(self):
        """Calculates rating average out of all reviewer scores."""
        if len(self.rating) != 0:
            self.total_rating = sum([self.rating[key] for key in self.rating])/len(self.rating)
