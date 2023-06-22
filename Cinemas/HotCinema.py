import json
import datetime

from Cinemas.Cinema import Cinema
from Functions import is_english, regexify, is_address_in_range, find_nearest_addresses, format_date, IMAGE_NOT_FOUND, \
    suffixify
from Movie import Movie


class HotCinema(Cinema):
    def __init__(self):
        super().__init__()
        self.home_url = 'https://hotcinema.co.il/'
        self.api_url = '{home_url}tickets/TheaterEvents2'.format(home_url=self.home_url)
        self.name = 'Hot Cinema'
        self.total_progress = 0
        self.progress = 0
        self.xpaths.update({'maps_url': ["//div[@class='text-wrapper']/a/@href"],
                            'trailer': ["//div[@class='ytp-title-text']/a/@href"],
                            'url': ["//div[@class='modal-body']/ul/li/a/@href"],
                            'title': ["//div[@class='modal-body']/ul/li/a/text()"]})

    def get_movies(self):
        response = self.get(self.home_url)
        movies = json.loads(regexify(regex='app.movies = (.*])', data=response.text))
        movies_list = []
        for x in movies:
            title = regexify(regex='/movie/\d*/(.*)', data=x['PageUrl'])
            if is_english(title):
                movies_list.append(Movie(title=title.replace('-', ' ').lower(),
                                         suffix=suffixify(title),
                                         image=IMAGE_NOT_FOUND,
                                         trailer=self.html.get_xpath_element_by_index(self.xpaths['trailer']),
                                         genre=[],
                                         origin={'Hot Cinema': x['ID']}))
        return movies_list

    def get_nearest_theatres(self):
        """Gets a list of cinema branches by id, latitude, longitude and display name.
        Then filters out branches that are outside a 20 km radius.
        Returns list of dictionaries as such:
        [{id:'', latitude:'', longitude:'', displayName:'', url:''}]"""

        response = self.get(self.home_url)
        urls = self.html.get_xpath_elements(self.xpaths['url'])
        urls = [url[1:] for url in urls]
        display_names = self.html.get_xpath_elements(self.xpaths['title'])
        theatres = []
        for x in range(len(display_names)):
            theatres.append({'displayName': display_names[x], 'url': self.home_url+urls[x]})
        # Nearest theatres will be done in next function.
        for theatre in theatres:
            response = self.get(theatre['url'])
            maps_url = self.html.get_xpath_element_by_index(self.xpaths['maps_url'], 1)
            theatre['latitude'], theatre['longitude'] = regexify(r'@([^,]+),([^,]+)', maps_url)
            theatre['latitude'], theatre['longitude'] = float(theatre['latitude']), float(theatre['longitude'])
            theatre['id'] = regexify(r'(?<=/)\d+', theatre['url'])

        # nearest_theatres = find_nearest_addresses(theatres)
        nearest_theatres = None
        return theatres if not nearest_theatres else nearest_theatres

    def get_theatre_screenings(self, theatres, movies=None):
        """Gets all movie screenings from theatres list.
        Returns dictionary which values are a list of dictionaries as such:
        {theatre1:{movieid1: screenings, movieid2: screenings...}, theatre2:{movieid3: screenings}}"""

        timetables = dict()
        today_date = datetime.datetime.now().strftime('%d/%m/%Y')
        self.total_progress = len(theatres)
        for theatre in theatres:
            url = '{api_url}?movieid=undefined&date={date}&theatreid={id}&site=undefined&time=&type=undefined&lang=&kinorai=undefined&genreId=0&screentype=&subdub=&isnew=false'.format(
                date=today_date, id=theatre['id'], api_url=self.api_url)
            response = self.get(url)
            events = json.loads(response.text)['TheaterEvents']

            timetable = {event['MovieId']: [] for event in events}

            for event in events:
                timetable[event['MovieId']].extend([event_date['Hour'] for event_date in event['Dates']])
            timetables[theatre['displayName']] = timetable
            self.progress += 1
        return timetables
