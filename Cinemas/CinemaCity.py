import datetime
import json
from collections import defaultdict

import bs4
from Cinemas.Cinema import Cinema
from Functions import is_english, regexify, find_nearest_addresses, IMAGE_NOT_FOUND, suffixify, capitalize_sentence
from Movie import Movie
from lxml import etree


class CinemaCity(Cinema):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.cinema-city.co.il/'
        self.api_url = 'https://tickets.cinema-city.co.il/api/presentations'
        self.name = 'Cinema City'
        self.theatres = {}
        self.total_progress = 0

    def get_amount_of_movies(self):
        response = self.get('{api_url}?VenueTypeId=1&Date=0'.format(api_url=self.api_url))
        response = json.loads(response.text)
        return len(response)

    def get_movies(self):
        response = self.get(self.api_url)
        self.html.set(response)
        response = json.loads(response.text)['presentations']
        self.html.response = response
        movies = {data['featureId']: data['featureAdditionalName'] for data in response}
        movies = {id: capitalize_sentence(movies[id]) for id in movies if is_english(movies[id])}
        return [Movie(title=movies[id],
                      suffix=suffixify(movies[id]),
                      trailer='',
                      genre=[],
                      image=IMAGE_NOT_FOUND,
                      origin={self.name: str(id)}) for id in movies]

    def get_nearest_theatres(self):
        """Gets a list of cinema branches by id, latitude, longitude and display name.
        Then filters out branches that are outside a 20 km radius.
        Returns list of dictionaries as such:
        [{id:'', latitude:'', longitude:'', displayName:'', url:''}]"""
        """Gets a list of cinema branches by id, latitude, longitude and display name.
        Then filters out branches that are outside a 20 km radius.
        Returns list of dictionaries as such:
        [{id:'', latitude:'', longitude:'', displayName:'', url:''}]"""
        theatres = list(set([data['locationName'] for data in self.html.response]))
        return theatres

    def get_theatre_screenings(self, theatres, movies=None):
        """Gets all movie screenings from theatres list.
        Returns dictionary which values are a list of dictionaries as such:
        {theatre1:{movieid1: screenings, movieid2: screenings...}, theatre2:{movieid3: screenings}}"""
        timetables = {key: dict() for key in theatres}
        today = datetime.datetime.now().date().strftime('%Y-%m-%d')
        for theatre in theatres:
            screenings = [(str(data['featureId']), regexify(r'\d{2}:\d{2}', data['dateTime'])) for data in
                          self.html.response
                          if data['locationName'] == theatre and
                          regexify(r'\d{4}-\d{2}-\d{2}', data['dateTime']) == today]
            movie_dict = defaultdict(list)
            for movie_id, time in screenings:
                movie_dict[movie_id].append(time)
                timetables[theatre] = dict(movie_dict)
            self.progress += 1
        return timetables
