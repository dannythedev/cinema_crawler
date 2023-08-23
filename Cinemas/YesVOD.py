import datetime
import json
import re
import urllib.parse

from Cinemas.Cinema import Cinema
from Functions import is_english, regexify, format_date, suffixify, IMAGE_NOT_FOUND
from Movie import Movie


class YesVOD(Cinema):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://www.yes.co.il'
        self.url = '{home_url}/content/main/movies'.format(home_url=self.home_url)
        self.name = 'Yes VOD'
        self.xpaths.update({'movies': ["//a[contains(@href,'content/movies')]/@href"]})
    def get_movies(self):
        movies_list = []
        response = self.get(self.url)
        token = regexify(r'authToken="(.*)";', response.text).split('";')[0]
        movies = self.html.get_xpath_elements(self.xpaths['movies'])
        self.api_url = '{home_url}/o/yes/servletlinearsched/getscheduale?startdate={date}&p_auth={token}'.format(
            home_url=self.home_url, date=datetime.date.today().strftime("%Y%m%d"), token=token)
        # TV Schedule
        response = self.get(self.api_url)

        # Movie VOD Schedule
        for movie in movies:
            suffix = urllib.parse.unquote(suffixify(re.sub(r"_\((.*?)\)", "", movie.split('/')[-1])))
            id = movie.split('/')[-2]
            movies_list.append(Movie(title=suffix.replace('_', ' '),
                      suffix=suffix.replace(' ', '_'),
                      image=IMAGE_NOT_FOUND,
                                     trailer='',
                                     genre=[],
                                     origin={self.name: str(id)}))
        return movies_list

    def get_nearest_theatres(self):
        """Gets a list of cinema branches by id, latitude, longitude and display name.
        Then filters out branches that are outside a 20 km radius.
        Returns list of dictionaries as such:
        [{id:'', latitude:'', longitude:'', displayName:'', url:''}]"""

        return []

    def get_theatre_screenings(self, theatres, movies=None):
        """Gets all movie screenings from theatres list.
        Returns dictionary which values are a list of dictionaries as such:
        {theatre1:{movieid1: screenings, movieid2: screenings...}, theatre2:{movieid3: screenings}}"""

        return dict()



