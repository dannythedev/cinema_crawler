import datetime
import json

import bs4
from Cinemas.Cinema import Cinema
from Functions import is_english, regexify, find_nearest_addresses, IMAGE_NOT_FOUND, suffixify, filter_hour_format, \
    sort_and_remove_duplicate_hours
from Movie import Movie
from lxml import etree

from app import is_image_url


class LevCinema(Cinema):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.lev.co.il/'
        self.url = '{home_url}en/movies/'.format(home_url=self.home_url)
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
        response = self.get('{home_url}cinemas/'.format(home_url=self.home_url))
        data = dict(zip(self.html.get_xpath("//p/a/img/@alt"), self.html.get_xpath("//p/a/@href")))
        return [{'id': '', 'latitude': '', 'longitude': '',
                 'displayName': key.replace('בית קולנוע', '').replace('שוהם', 'שהם').strip(), 'url': data[key].strip()} for key in data]

    def get_theatre_screenings(self, theatres, movies=None):
        """Gets all movie screenings from theatres list.
        Returns dictionary which values are a list of dictionaries as such:
        {theatre1:{movieid1: screenings, movieid2: screenings...}, theatre2:{movieid3: screenings}}"""

        timetables = dict()
        for theatre in theatres:
            timetables.update({theatre['displayName']:dict()})
        self.total_progress = len(theatres)
        for movie in movies:
            self.get(movie.url)
            theatres_in_movie = self.html.get_xpath("//div[@class='forloc 2']")
            theatres_in_movie = [etree.tostring(x, pretty_print=True) for x in theatres_in_movie]
            for theatre in theatres_in_movie:
                self.html.set(theatre)
                theatre_display_name = str(self.html.get_xpath("//div[@class='showlist 456'][1]//a[@class='mobilelink']/@data-loc")[0])
                screenings = filter_hour_format(self.html.get_xpath("//div[@class='showlist 456'][1]//a[@class='mobilelink']/text()"))
                timetables[theatre_display_name].update({movie.origin[self.name]:sort_and_remove_duplicate_hours(screenings)})
            self.progress+=1
        return timetables
