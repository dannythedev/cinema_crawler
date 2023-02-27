from Archive import Archive
import time
from threading import Thread

from Reviewers.IMDB import IMDB
from Reviewers.Metacritic import Metacritic
from Reviewers.RottenTomatoes import RottenTomatoes
from Cinemas.YesPlanet import YesPlanet

if __name__ == "__main__":
    start = time.time()
    cinema = YesPlanet()
    archive = Archive(movies=cinema.get_movies())

    reviewers = [Metacritic(), IMDB(), RottenTomatoes()]
    threads = []

    for reviewer in reviewers:
        threads.append(Thread(target=reviewer.initialize, args=[archive.movies]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    archive.sort_by_rating()
    archive.export_json()
    print('Time:', time.time()-start)

