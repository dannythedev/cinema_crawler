import datetime
import json
from collections import defaultdict

from Cinemas.Cinema import Cinema
from Functions import is_english, regexify, find_nearest_addresses, IMAGE_NOT_FOUND, suffixify, filter_hour_format, \
    sort_and_remove_duplicate_hours
from Movie import Movie
from lxml import etree
from Functions import is_image_url


class LevCinema(Cinema):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.lev.co.il/'
        self.url = '{home_url}en/movies/'.format(home_url=self.home_url)
        self.api_url = 'https://ticket.lev.co.il/api/presentations?includeSynopsis=0'
        self.name = 'Lev Cinema'

    def get_movies(self):
        response = self.get(self.url)
        movies = self.html.get_xpath("//div[@class='item']")
        movies = [etree.tostring(x, pretty_print=True) for x in movies]
        movie_ids = dict(zip(self.html.get_xpath("//div[@id='moviefilter']//option/text()"),
                             self.html.get_xpath("//div[@id='moviefilter']//option/@value")))
        movies_list = []
        for movie in movies:
            self.html.set(str(movie))
            title = self.html.get_xpath("//div[@class='movieInfo']/div[@class='movieName']/text()")[0].replace('\\n',
                                                                                                               '').strip()
            url = self.html.get_xpath("//a/@href")[0]
            image = self.html.get_xpath("//img/@src")[1] if is_image_url(
                self.html.get_xpath("//img/@src")[1]) else IMAGE_NOT_FOUND
            try:
                id = movie_ids[title.replace('–', '-')]
            except KeyError:
                continue
            movies_list.append(Movie(title=title,
                                     suffix=suffixify(title),
                                     image=image,
                                     trailer='',
                                     genre=[],
                                     origin={self.name: id}, url=url))
        movies_list = [movie for movie in movies_list if 'special event' not in movie.title.lower()]
        return movies_list

    def get_nearest_theatres(self):
        """Gets a list of cinema branches by id, latitude, longitude and display name.
        Then filters out branches that are outside a 20 km radius.
        Returns list of dictionaries as such:
        [{id:'', latitude:'', longitude:'', displayName:'', url:''}]"""
        response = self.get(self.api_url)
        self.html.set(response)
        response = json.loads(response.text)['presentations']
        self.html.response = response
        theatres = list(set([data['locationName'] for data in response]))
        return theatres

    def get_theatre_screenings(self, theatres, movies=None):
        """Gets all movie screenings from theatres list.
        Returns dictionary which values are a list of dictionaries as such:
        {theatre1:{movieid1: screenings, movieid2: screenings...}, theatre2:{movieid3: screenings}}"""

        timetables = {key: dict() for key in theatres}
        today = datetime.datetime.now().date().strftime('%Y-%m-%d')
        for theatre in theatres:
            screenings = [(str(data['featureId']), regexify(r'\d{2}:\d{2}', data['dateTime'])) for data in self.html.response
                          if data['locationName'] == theatre and
                          regexify(r'\d{4}-\d{2}-\d{2}',data['dateTime']) == today]
            movie_dict = defaultdict(list)
            for movie_id, time in screenings:
                movie_dict[movie_id].append(time)
                timetables[theatre] = dict(movie_dict)
            self.progress += 1
        return timetables
