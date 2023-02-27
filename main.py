from cinema.Archive import Archive
import time
from threading import Thread

from cinema.Reviewers.IMDB import IMDB
from cinema.Reviewers.Metacritic import Metacritic
from cinema.Reviewers.RottenTomatoes import RottenTomatoes
from cinema.Cinemas.YesPlanet import YesPlanet

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

